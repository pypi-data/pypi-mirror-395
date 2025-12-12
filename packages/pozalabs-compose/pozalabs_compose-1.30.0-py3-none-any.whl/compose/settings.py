from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from . import utils

if TYPE_CHECKING:
    import mypy_boto3_ssm


def get_parameters_from_ssm(
    ssm_client: mypy_boto3_ssm.SSMClient,
    prefix: str,
    preprocessors: dict[str, Callable[[str], str]] = None,
) -> dict[str, Any]:
    preprocessors = preprocessors or {}

    result = {}
    has_next = True
    next_token = None
    while has_next:
        params = {
            "Path": prefix,
            "WithDecryption": True,
            "Recursive": True,
        }
        if next_token is not None:
            params["NextToken"] = next_token

        response = ssm_client.get_parameters_by_path(**params)
        for parameter in response["Parameters"]:
            key = parameter["Name"].split("/")[-1].lower()
            value = parameter["Value"]
            result[key] = preprocessors.get(key, utils.ident)(value)

        next_token = response.get("NextToken")
        has_next = next_token is not None
    return result
