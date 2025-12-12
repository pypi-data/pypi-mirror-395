import logging
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import botocore.exceptions
from omegaconf import OmegaConf

from launcher.nova.launchers import NovaK8SLauncher
from main import main

logger = logging.getLogger(__name__)

import pytest

from tests.test_utils import (
    compare_artifacts,
    create_temp_directory,
    make_hydra_cfg_instance,
)

sft_run_name = "nova-lite-sft"


@pytest.fixture(autouse=True)
def mock_aws_account_id():
    with patch("launcher.nova.launchers.boto3.client") as mock_boto_client:
        mock_boto_client.return_value.get_caller_identity.return_value = {"Account": "123456789012"}
        yield


@pytest.fixture(autouse=True)
def mock_aws_region():
    session_mock = MagicMock()
    session_mock.region_name = "us-east-1"

    with patch("launcher.nova.launchers.boto3.session.Session", return_value=session_mock):
        yield


@contextmanager
def mock_aws_account_id_invalid():
    with patch("launcher.nova.launchers.boto3.client") as mock_boto_client:
        mock_boto_client.return_value.get_caller_identity.side_effect = botocore.exceptions.NoCredentialsError()
        yield


def compare_sft_recipe_k8s_artifacts(artifacts_dir):
    logger.info("Comparing sft recipe k8s artifacts")

    artifacts_paths = [
        f"/{sft_run_name}/{sft_run_name}_launch.sh",
        f"/{sft_run_name}/k8s_templates/values.yaml",
        f"/{sft_run_name}/k8s_templates/Chart.yaml",
        f"/{sft_run_name}/k8s_templates/templates/training.yaml",
        f"/{sft_run_name}/k8s_templates/templates/training-config.yaml",
    ]

    k8s_baseline_artifacts_path = "/tests/nova_k8s_workflow/k8s_baseline_artifacts"
    compare_artifacts(artifacts_paths, artifacts_dir, k8s_baseline_artifacts_path)


def test_sft_recipe_k8s_workflow():
    logger.info("Testing SFT recipe k8s workflow")

    artifacts_dir = create_temp_directory()
    overrides = [
        "instance_type=p5.48xlarge",
        "recipes=fine-tuning/nova/nova_lite_p5_gpu_sft",
        f"recipes.run.name={sft_run_name}",
        "base_results_dir={}".format(artifacts_dir),
        "container=test_container",
        "cluster=k8s",
        "cluster_type=k8s",
        "+cluster.service_account_name=default",
        "+cluster.priority_class_name=test_pc_name",
        "+cluster.annotations.annotation_key_1=annotation-value-1",
        "+cluster.custom_labels.label_key_1=label-value-1",
        "+cluster.label_selector.required.example_label_key=[expected-label-value-1, expected-label-value-2]",
    ]

    sample_recipe_k8s_config = make_hydra_cfg_instance("../recipes_collection", "config", overrides)

    logger.info("\nsample_recipe_k8s_config\n")
    logger.info(OmegaConf.to_yaml(sample_recipe_k8s_config))

    main(sample_recipe_k8s_config)

    compare_sft_recipe_k8s_artifacts(artifacts_dir)


def test_recipe_k8s_workflow_invalid():
    logger.info("Testing recipe k8s workflow with invalid git config")
    overrides = [
        "instance_type=p5.48xlarge",
        "recipes=fine-tuning/nova/nova_lite_p5_gpu_sft",
        f"recipes.run.name={sft_run_name}",
        "+cluster.persistent_volume_claims.0.claimName=fsx-claim",
        "+cluster.persistent_volume_claims.0.mountPath=data",
        "cluster=k8s",
        "cluster_type=k8s",
    ]

    sample_recipe_k8s_config = make_hydra_cfg_instance("../recipes_collection", "config", overrides)

    logger.info("\nsample_recipe_k8s_config\n")
    logger.info(OmegaConf.to_yaml(sample_recipe_k8s_config))
    with pytest.raises(ValueError):
        main(sample_recipe_k8s_config)


def test_recipe_env_vars():
    with mock_aws_account_id_invalid():
        logger.info("Testing SFT recipe k8s workflow")

        artifacts_dir = create_temp_directory()
        overrides = [
            "instance_type=p5.48xlarge",
            "recipes=fine-tuning/nova/nova_lite_p5_gpu_sft",
            f"recipes.run.name={sft_run_name}",
            "base_results_dir={}".format(artifacts_dir),
            "container=test_container",
            "cluster=k8s",
            "cluster_type=k8s",
            "+cluster.service_account_name=default",
            "+cluster.priority_class_name=test_pc_name",
            "+cluster.annotations.annotation_key_1=annotation-value-1",
            "+cluster.custom_labels.label_key_1=label-value-1",
            "+cluster.label_selector.required.example_label_key=[expected-label-value-1, expected-label-value-2]",
        ]

        sample_recipe_k8s_config = make_hydra_cfg_instance("../recipes_collection", "config", overrides)

        base_class = NovaK8SLauncher(sample_recipe_k8s_config)
        result = base_class._get_env_vars()
        assert result == {}
