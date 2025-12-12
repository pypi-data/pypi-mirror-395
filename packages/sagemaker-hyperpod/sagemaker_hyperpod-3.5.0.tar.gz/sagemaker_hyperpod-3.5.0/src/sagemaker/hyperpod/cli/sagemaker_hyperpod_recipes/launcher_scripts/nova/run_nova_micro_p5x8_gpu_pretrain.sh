#!/bin/bash
set -e

SAGEMAKER_TRAINING_LAUNCHER_DIR=${SAGEMAKER_TRAINING_LAUNCHER_DIR:-"$(pwd)"}

HYDRA_FULL_ERROR=1 python3 "${SAGEMAKER_TRAINING_LAUNCHER_DIR}/main.py" \
    recipes=training/nova/nova_micro_p5x8_gpu_pretrain \
    base_results_dir="${SAGEMAKER_TRAINING_LAUNCHER_DIR}/results"
