#!/usr/bin/env python3
"""Run a task from a yaml config file."""

from __future__ import annotations

import ast
import json
from os import PathLike
from typing import Any, Dict, Optional, Union

import fire

from bitfount import config
from bitfount.runners.modeller_runner import (
    run_modeller,
    setup_modeller_from_config_file,
)
from bitfount.utils.logging_utils import log_pytorch_env_info_if_available

config._BITFOUNT_CLI_MODE = True


def _parse_template_params(params_str: Union[str, Dict]) -> Any:
    """Parse template parameters from string or dict input.

    Args:
        params_str: Template parameters as a JSON string or dictionary.

    Returns:
        Parsed template parameters as a dictionary.

    Raises:
        ValueError: If the parameters cannot be parsed.
    """
    if isinstance(params_str, dict):
        return params_str

    try:
        # Try to parse as JSON
        return json.loads(params_str)
    except json.JSONDecodeError:
        try:
            # Try to parse as Python literal
            return ast.literal_eval(params_str)
        except (SyntaxError, ValueError) as err_parse:
            raise ValueError(
                f"Cannot parse template parameters: {params_str}"
            ) from err_parse


def run(
    path_to_config_yaml: Union[str, PathLike],
    require_all_pods: bool = False,
    pod_identifier: Optional[str] = None,
    project_id: Optional[str] = None,
    template_params: Optional[Union[str, Dict[str, Any]]] = None,
) -> None:
    """Runs a modeller from a config file.

    Args:
        path_to_config_yaml: Path to the config YAML file.
        require_all_pods: Whether to require all pods to accept the task before
            continuing.
        pod_identifier: Optional pod identifier to use instead of the one in the config.
        project_id: Optional project ID to use instead of the one in the config.
        template_params: Optional dictionary mapping template parameter names to values.
    """
    log_pytorch_env_info_if_available()

    # Parse template parameters if provided
    parsed_template_params = None
    if template_params:
        parsed_template_params = _parse_template_params(template_params)

    (
        modeller,
        pod_identifiers,
        project_id,
        run_on_new_datapoints,
        batched_execution,
        test_run,
        force_rerun_failed_files,
    ) = setup_modeller_from_config_file(
        path_to_config_yaml, pod_identifier, project_id, parsed_template_params
    )

    run_modeller(
        modeller,
        pod_identifiers,
        require_all_pods,
        project_id,
        run_on_new_datapoints,
        batched_execution,
        test_run,
        force_rerun_failed_files,
    )


if __name__ == "__main__":
    fire.Fire(run)
