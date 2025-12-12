import logging
from unittest.mock import MagicMock, patch

import pytest
from omegaconf import OmegaConf

from main import main

logger = logging.getLogger(__name__)

from tests.test_utils import (
    compare_artifacts,
    create_temp_directory,
    make_hydra_cfg_instance,
)

ppo_run_name = "nova-lite-ppo"


@pytest.fixture(autouse=True)
def mock_aws_region():
    session_mock = MagicMock()
    session_mock.region_name = "us-east-1"

    with patch("launcher.nova.launchers.boto3.session.Session", return_value=session_mock):
        yield


def compare_ppo_recipe_k8s_artifacts(artifacts_dir):
    logger.info("Comparing ppo recipe k8s artifacts")

    artifacts_paths = [
        f"/{ppo_run_name}/{ppo_run_name}_launch.sh",
        f"/{ppo_run_name}/k8s_templates/values.yaml",
        f"/{ppo_run_name}/k8s_templates/Chart.yaml",
        f"/{ppo_run_name}/k8s_templates/templates/training.yaml",
        f"/{ppo_run_name}/k8s_templates/templates/training-ag.yaml",
        f"/{ppo_run_name}/k8s_templates/templates/training-config.yaml",
    ]

    k8s_baseline_artifacts_path = "/tests/nova_k8s_workflow/k8s_baseline_artifacts"
    compare_artifacts(artifacts_paths, artifacts_dir, k8s_baseline_artifacts_path)


def test_ppo_recipe_k8s_workflow():
    logger.info("Testing PPO recipe k8s workflow")

    artifacts_dir = create_temp_directory()
    overrides = [
        "instance_type=p5.48xlarge",
        "recipes=fine-tuning/nova/nova_pro_p5_gpu_ppo",
        f"recipes.run.name={ppo_run_name}",
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
    compare_ppo_recipe_k8s_artifacts(artifacts_dir)
