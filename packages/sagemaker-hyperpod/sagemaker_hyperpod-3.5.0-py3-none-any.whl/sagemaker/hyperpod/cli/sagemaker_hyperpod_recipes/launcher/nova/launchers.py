# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import copy
import logging
import os
import shutil
import subprocess
from abc import abstractmethod
from pathlib import Path
from typing import Dict, List

import boto3
import omegaconf
from botocore.exceptions import BotoCoreError, ClientError
from omegaconf import DictConfig, OmegaConf

from .constants.ppo_container_constants import (
    JOB_TASK_TYPE_DICT,
    JOB_TYPE_DICT,
    KEYS_TO_REMOVE,
    JobType,
)
from .utils import get_actor_generation_container_uri, get_init_container_uri

logger = logging.getLogger(__name__)


class NovaK8SLauncher:
    """
    Base class for Nova Kubernetes Launchers that provides common functionality for deploying Nova jobs on K8s clusters, handling AWS account integration, environment variables, and Helm chart generation.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self._job_name = cfg.recipes.run["name"]
        self._output_dir = Path(cfg["base_results_dir"]) / self._job_name
        self._output_dir_k8s_folder = self._output_dir / "k8s_templates"
        # Try to get the region using boto3 session or env var
        self._init_container_uri = get_init_container_uri()

    @staticmethod
    def _get_aws_account_id():
        """Returns the AWS account ID for the current credentials."""
        try:
            sts = boto3.client("sts")
            return sts.get_caller_identity()["Account"]
        except (BotoCoreError, ClientError) as e:
            print(f"Error retrieving AWS account ID: {e}")
            return None

    def _get_env_vars(self):
        """Returns a dictionary of environment variables to inject."""
        account_id = self._get_aws_account_id()
        if account_id:
            return {"X_AMZ_SOURCE_ACCOUNT": account_id}
        return {}

    def _prepare_output_dir(self):
        if self._output_dir_k8s_folder.exists():
            shutil.rmtree(self._output_dir_k8s_folder)
        os.makedirs(self._output_dir_k8s_folder / "templates", exist_ok=True)
        logger.info(f"Prepared output directory at {self._output_dir_k8s_folder}")

    def _interpolate_hydra(self):
        def interpolate(cfg):
            if isinstance(cfg, DictConfig):
                for k, v in cfg.items():
                    cfg[k] = interpolate(v)
            elif isinstance(cfg, list):
                for i, v in enumerate(cfg):
                    cfg[i] = interpolate(v)
            return cfg

        interpolate(self.cfg.recipes)

    def _create_chart_file(self, template_dir):
        static_chart = template_dir / "Chart.yaml"
        if static_chart.exists():
            shutil.copyfile(static_chart, self._output_dir_k8s_folder / "Chart.yaml")

    def _write_value_template(self, values_template):
        """
        Write the value template into disk
        """
        k8s_template_file = Path(self._output_dir_k8s_folder) / "values.yaml"
        k8s_template_file.parent.mkdir(parents=True, exist_ok=True)

        conf = OmegaConf.create(values_template)
        OmegaConf.save(conf, k8s_template_file)

    def _create_helm_script(self, chart_path: Path):
        script_path = self._output_dir / f"{self._job_name}_launch.sh"
        job_name = self._job_name.replace("_", "-")

        extra_helm_args = ""
        if self.cfg.cluster.get("namespace"):
            extra_helm_args += f" --namespace {self.cfg.cluster['namespace']}"

        helm_command = f"#!/bin/bash\n" f"helm install --timeout=15m {extra_helm_args} {job_name} {chart_path}\n"

        script_path.write_text(helm_command)
        script_path.chmod(0o755)
        logger.info(f"Helm script created at {script_path}")
        return script_path

    def _get_label_selectors(self):
        """
        Constructs and returns a dictionary of label selectors required for Nova jobs.

        This method ensures that the returned label selectors always include the required
        instance types and instance group types necessary for Nova jobs to run on the
        appropriate hardware. It merges any user-provided required label selectors from
        the configuration with the hardcoded required labels.

        Returns:
            dict: A dictionary containing the merged label selectors, with the "required"
            key including both user-specified and mandatory labels.
        """

        # Default instance types for required labels
        # Nova jobs cannot be run on any other instance types apart from these
        # This is a hard requirement for the Nova jobs to run
        # on the required hardware.
        required_instances = {
            "node.kubernetes.io/instance-type": ["ml.p5.48xlarge"],
            "sagemaker.amazonaws.com/instance-group-type": ["Restricted"],
        }

        # Handle labelSelector merging safely
        label_selector = self.cfg.cluster.get("label_selector") or {}
        required_labels = label_selector.get("required") or {}
        return {
            **label_selector,
            "required": {**required_labels, **required_instances},
        }

    @staticmethod
    def _run_helm_script(script_path: Path):
        logger.info(f"Running Helm script: {script_path}")
        subprocess.Popen(str(script_path)).wait()

    @abstractmethod
    def _save_hydra_config(self):
        pass  # pragma: no cover

    @abstractmethod
    def run(self):
        """Generate a Helm-installable k8s_template directory."""
        pass  # pragma: no cover

    @abstractmethod
    def _copy_k8s_template(self):
        """copy helm files in k8s_template directory."""
        pass  # pragma: no cover

    @abstractmethod
    def _process_values_yaml(self):
        """Generate values based on training type for values.yaml file."""
        pass  # pragma: no cover


class SMNovaK8SLauncherSFT(NovaK8SLauncher):
    """
    Launcher for Supervised Fine-Tuning (SFT) jobs on Kubernetes that handles deployment of SFT training jobs with proper configuration, container setup, and node allocation.
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        self._template_dir = Path(__file__).parent / "k8s_templates/SFT"

    def run(self):
        self._prepare_output_dir()
        self._save_hydra_config()
        self._create_chart_file(self._template_dir)
        self._copy_k8s_template()
        self._process_values_yaml()
        script_path = self._create_helm_script(self._output_dir_k8s_folder)
        self._run_helm_script(script_path)
        logger.info(f"Launcher successfully generated: {self._template_dir}")

    def _save_hydra_config(self):
        self._interpolate_hydra()
        config_path = Path(self._output_dir_k8s_folder / "config")
        config_path.mkdir(parents=True, exist_ok=True)
        config_file = Path(config_path / f"{self._job_name}_hydra.yaml")
        omegaconf.OmegaConf.save(self.cfg.recipes, config_file)

    def _copy_k8s_template(self):
        for fname in ["training.yaml", "training-config.yaml"]:
            src = self._template_dir / fname
            dst = self._output_dir_k8s_folder / "templates" / fname
            shutil.copyfile(src, dst)

    def _process_values_yaml(self):
        # Load values.yaml template
        with open(self._template_dir / "values.yaml") as value_file:
            values_template = OmegaConf.load(value_file)

        cluster_cfg = copy.deepcopy(self.cfg.get("cluster") or {})
        k8s_cfg = {**cluster_cfg}

        # Basic assignments
        values_template.image.trainingImage = self.cfg.get("container")
        values_template.trainingConfig.jobName = self._job_name
        values_template.trainingConfig.initContainer.image = self._init_container_uri
        values_template.trainingConfig.envVars = self._get_env_vars()

        # Default is 8 if we dont find value in resource_config.devices or training_config.trainer.devices
        # resource_config is for eval recipes
        # training_config.trainer is for training recipes
        values_template.trainingConfig.devices = (
            OmegaConf.select(self.cfg, "recipes.resource_config.devices")
            or OmegaConf.select(self.cfg, "recipes.training_config.trainer.devices")
            or 8
        )
        # Replicas: always at least one node
        num_nodes = OmegaConf.select(self.cfg, "recipes.run.replicas", default=0)
        values_template.trainingConfig.worker_nodes = max(num_nodes - 1, 0)

        # Optional K8s fields
        optional_fields = {
            "namespace": "namespace",
            "annotations": "annotations",
            "priority_class_name": "priorityClassName",
            "service_account_name": "serviceAccountName",
            "custom_labels": "customLabels",
        }

        for src, dest in optional_fields.items():
            val = k8s_cfg.get(src)
            if val is not None:
                setattr(values_template.trainingConfig, dest, val)

        values_template.trainingConfig.labelSelector = self._get_label_selectors()
        self._write_value_template(values_template)


class SMNovaK8SLauncherPPO(NovaK8SLauncher):
    """
    Launcher for Proximal Policy Optimization (PPO) jobs on Kubernetes that manages complex multi-job deployments including reward models, critic models, actor generation and training with appropriate resource allocation.
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        self._template_dir = Path(__file__).parent / "k8s_templates/PPO"
        self._reward_model_job_name = f"${self._job_name}_rm"
        self._critic_model_job_name = f"${self._job_name}_cm"
        self._anchor_model_job_name = f"${self._job_name}_am"
        self._actor_generation_job_name = f"${self._job_name}_ag"
        self._actor_train_job_name = f"${self._job_name}_at"
        self._actor_generation_container_uri = get_actor_generation_container_uri()

    def _save_hydra_config(self):
        """
        Saves the Hydra configuration for the current job.

        This method performs the following steps:
        1. Interpolates the Hydra configuration.
        2. Creates a 'config' directory inside the Kubernetes output folder if it does not exist.
        3. Converts the 'run' recipe configuration to a dictionary, resolving all interpolations.
        4. Removes specific keys defined in KEYS_TO_REMOVE from the run configuration.
        5. For each job type defined in JOB_TYPE_DICT:
            - Converts the corresponding recipe configuration to a dictionary.
            - Sets the 'task_type' field based on JOB_TASK_TYPE_DICT.
            - Builds a new configuration dictionary containing both 'run' and 'training_config'.
            - Saves the configuration as a YAML file named with the job name and job type.
        """
        self._interpolate_hydra()
        config_path = Path(self._output_dir_k8s_folder / "config")
        config_path.mkdir(parents=True, exist_ok=True)
        # Start building the new config
        run_config = omegaconf.OmegaConf.to_container(self.cfg.recipes.run, resolve=True)

        for key in KEYS_TO_REMOVE:
            run_config.pop(key, None)
        # Build final config
        new_config_dict = {"run": run_config}
        for key, value in JOB_TYPE_DICT.items():
            config_file = Path(config_path / f"{self._job_name}-{key.value}_hydra.yaml")
            training_config = omegaconf.OmegaConf.to_container(self.cfg.recipes[value])
            training_config["task_type"] = JOB_TASK_TYPE_DICT[key]
            new_config_dict["training_config"] = training_config
            omegaconf.OmegaConf.save(new_config_dict, config_file)

    def _build_job_list(self) -> List[Dict]:
        """
        Constructs a list of job configurations for different job types defined in `JOB_TYPE_DICT`.

        Each job dictionary contains:
        - `jobName`: A unique job name composed of the base job name and job type.
        - `master_nodes`: Number of master nodes. For `JobType.ACTOR_GENERATION`, it uses the full node count; otherwise, it's 1.
        - `worker_nodes`: Number of worker nodes, calculated as (nodes - 1), but not less than 0.
        - `devices`: Number of devices (e.g., GPUs) per job, defaulting to 8 if unspecified.

        The values for `nodes` and `devices` are retrieved from a hierarchical config (Hydra OmegaConf),
        using paths from recipe `recipes.<task_name>.trainer.num_nodes`.

        Returns:
            List[Dict]: A list of dictionaries, each representing a job configuration with keys:
                - "jobName": The name of the job (str)
                - "master_nodes": Number of master nodes (int)
                - "worker_nodes": Number of worker nodes (int)
                - "devices": Number of devices per node (int)
        """
        job_list = []

        for job_type in JOB_TYPE_DICT.keys():
            task_name = JOB_TYPE_DICT.get(job_type)
            if not task_name:
                continue

            nodes = OmegaConf.select(self.cfg, f"recipes.{task_name}.trainer.num_nodes", default=0)
            devices = OmegaConf.select(self.cfg, f"recipes.{task_name}.trainer.devices", default=8)
            master_nodes = nodes if job_type == JobType.ACTOR_GENERATION else 1
            worker_nodes = max(0, nodes - 1)

            job_list.append(
                {
                    "jobName": f"{self._job_name}-{job_type.value}",
                    "master_nodes": master_nodes,
                    "worker_nodes": worker_nodes,
                    "devices": devices,
                }
            )

        return job_list

    def _process_values_yaml(self):
        # Load values.yaml as an OmegaConf object
        with open(self._template_dir / "values.yaml") as value_file:
            values_template = OmegaConf.load(value_file)

        # Deep copy cluster config for isolation
        cluster_cfg = self.cfg.get("cluster") or {}
        k8s_cfg = copy.deepcopy(cluster_cfg)

        # Assign base container config
        values_template.image.trainingImage = self.cfg.get("container")
        values_template.image.actor_generation_image = self._actor_generation_container_uri

        # Assign job-specific values
        values_template.trainingConfig.jobName = self._job_name
        values_template.trainingConfig.initContainer.image = self._init_container_uri
        values_template["jobList"] = self._build_job_list()

        # Optional fields mapping
        field_mapping = {
            "namespace": "namespace",
            "annotations": "annotations",
            "priority_class_name": "priorityClassName",
            "service_account_name": "serviceAccountName",
            "custom_labels": "customLabels",
        }

        for key, attr in field_mapping.items():
            val = k8s_cfg.get(key)
            if val is not None:
                setattr(values_template.trainingConfig, attr, val)

        values_template.trainingConfig.labelSelector = self._get_label_selectors()

        self._write_value_template(values_template)

    def _copy_k8s_template(self):
        for fname in ["training.yaml", "training-ag.yaml", "training-config.yaml"]:
            src = self._template_dir / fname
            dst = self._output_dir_k8s_folder / "templates" / fname
            shutil.copyfile(src, dst)

    def run(self):
        self._prepare_output_dir()
        self._save_hydra_config()
        self._create_chart_file(self._template_dir)
        self._copy_k8s_template()
        self._process_values_yaml()
        script_path = self._create_helm_script(self._output_dir_k8s_folder)
        self._run_helm_script(script_path)
