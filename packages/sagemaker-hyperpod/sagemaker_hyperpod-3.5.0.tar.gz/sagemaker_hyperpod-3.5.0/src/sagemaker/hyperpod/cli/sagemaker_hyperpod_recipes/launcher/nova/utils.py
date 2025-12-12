import os

import boto3

from launcher.nova.constants.init_container_constants import (
    INIT_CONTAINER_IMAGE_URI,
    INIT_CONTAINER_REGION_ACCOUNT_MAP,
)
from launcher.nova.constants.ppo_container_constants import (
    ACTOR_GENERATION_CONTAINER_IMAGE,
    ACTOR_GENERATION_REGION_ACCOUNT_MAP,
)


def get_current_region():
    region = boto3.session.Session().region_name or os.environ.get("AWS_REGION")

    if not region:
        raise ValueError("AWS region could not be determined during initialization.")
    return region


def get_actor_generation_container_uri() -> str:
    region = get_current_region()

    account_id = ACTOR_GENERATION_REGION_ACCOUNT_MAP.get(region)
    if not account_id:
        raise ValueError(f"Nova recipes are not supported for region '{region}'.")

    return ACTOR_GENERATION_CONTAINER_IMAGE.format(account_id=account_id, region=region)


def get_init_container_uri() -> str:
    region = get_current_region()

    account_id = INIT_CONTAINER_REGION_ACCOUNT_MAP.get(region)
    if not account_id:
        raise ValueError(f"Nova recipes are not supported for region '{region}'.")

    return INIT_CONTAINER_IMAGE_URI.format(account_id=account_id, region=region)
