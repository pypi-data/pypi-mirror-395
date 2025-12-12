import os
from typing import Literal


def get_env_var(key: str) -> str | None:
    return os.environ.get(key)


def get_environment() -> Literal["development", "production"]:
    branch = os.environ.get("CI_COMMIT_REF_NAME", "default")
    return "production" if branch == "trunk" else "development"


def get_version() -> str:
    return os.environ.get("CI_COMMIT_SHA", "00000000")[:8]


def set_product_id(product_id: str) -> None:
    os.environ["PRODUCT_ID"] = product_id


def set_commit_sha(commit_sha: str) -> None:
    os.environ["CI_COMMIT_SHA"] = commit_sha


def set_commit_ref_name(commit_ref_name: str) -> None:
    os.environ["CI_COMMIT_REF_NAME"] = commit_ref_name
