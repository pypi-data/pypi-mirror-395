"""Utility functions related to config YAML specification classes."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional, Union, overload

import marshmallow
from marshmallow.decorators import POST_LOAD
import pydash

from bitfount.types import _JSON
from bitfount.utils import invert_dict, str_is_int

_logger = logging.getLogger(__name__)


@overload
def _deserialize_path(path: str, context: Optional[dict[str, Any]] = None) -> Path: ...


@overload
def _deserialize_path(path: None, context: Optional[dict[str, Any]] = None) -> None: ...


def _deserialize_path(
    path: Optional[str], context: Optional[dict[str, Any]] = None
) -> Optional[Path]:
    """Converts a str into a Path.

    If the input is None, the output is None.

    If the path to the config file is supplied in the `context` dict (in the
    "config_path" key) then any relative paths will be resolved relative to the
    directory containing the config file. If context is not provided or doesn't
    contain "config_path", relative paths will be resolved relative to the current
    working directory.

    Args:
        path: The path string to deserialize, or None
        context: Optional context dict that may contain "config_path" key

    Returns:
        A Path object, or None if path is None
    """
    if path is None:
        return None

    ppath = Path(path)

    # If relative path, use relative to config file if present in context
    if not ppath.is_absolute() and context and "config_path" in context:
        config_dir = Path(context["config_path"]).parent
        orig_ppath = ppath
        ppath = config_dir.joinpath(ppath).resolve()
        _logger.debug(
            f"Making relative paths relative to {config_dir}: {orig_ppath} -> {ppath}"
        )

    return ppath.expanduser()


def _deserialize_model_ref(ref: str) -> Union[Path, str]:
    """Deserializes a model reference.

    If the reference is a path to a file (and that file exists), return a Path
    instance. Otherwise, returns the str reference unchanged.
    """
    path = Path(ref).expanduser()
    if path.is_file():  # also returns False if path doesn't exist
        return path
    else:
        return ref


def keep_desert_output_as_dict(
    clazz: type[marshmallow.Schema],
) -> type[marshmallow.Schema]:
    """Make a desert schema deserialize as a dict.

    Normally `desert` will deserialize back into the dataclass that was used to
    generate the schema in the first place. However, there are times when we want to
    _specify_ the schema via a dataclass (for simplicity), but _use_ the schema as a
    dict. We could simply call `asdict()` on the deserialized dataclass but if the
    instance is nested deep within an object this may be tricky or not preferable.

    This function works by modifying the registered hooks on the schema class to
    remove the "make_data_class" `post_load` hook that `desert` has added.
    """
    # Find the index of the @post_load hook that desert added
    match_idx = -1
    for idx, (attr_name, _hook_many, _processor_kwargs) in enumerate(
        clazz._hooks[POST_LOAD]
    ):
        if attr_name == "make_data_class":
            match_idx = idx
            break
    else:
        # If it wasn't found, log out details. It may be that something internal to
        # desert has changed, or perhaps this just wasn't a desert schema?
        post_load_hooks: list[str] = [
            name for name, hook_many, processor_kwargs in clazz._hooks[POST_LOAD]
        ]
        post_load_hooks_names: str = (
            ", ".join('"' + s + '"' for s in post_load_hooks)
            if post_load_hooks
            else "no @post_load hooks"
        )
        _logger.warning(
            f"Passed class {clazz} did not have the @post_load hook expected"
            f" for desert-created schema classes;"
            f' expected "make_data_class",'
            f" got {post_load_hooks_names}"
        )
    # Remove the hook, if found
    if match_idx != -1:
        clazz._hooks[POST_LOAD].pop(match_idx)
    return clazz


def get_pydash_deep_paths(
    obj: _JSON,
) -> dict[str, str | int | float | bool | None]:
    """Produce a map of pydash deep path strings to values for a given JSON object.

    Output keys will be deep path strings per
    https://pydash.readthedocs.io/en/stable/deeppath.html.
    """

    def _recursive_pydash_deep_paths(
        obj_: _JSON,
        curr_path_: tuple[str, ...],
        root_dict_: dict[tuple[str, ...], str | int | float | bool | None],
    ) -> None:
        # Recurse into dict values, with their keys appended to path
        if isinstance(obj_, dict):
            for k, v in obj_.items():
                # k is a string, but if it could be ambiguously misunderstood as an int
                # we need to wrap it in square brackets per
                # https://pydash.readthedocs.io/en/stable/deeppath.html
                k_entry = k
                if str_is_int(k):
                    k_entry = f"[{k_entry}]"

                _recursive_pydash_deep_paths(v, curr_path_ + (k_entry,), root_dict_)
        # Recurse into list values, with their index appended to path
        elif isinstance(obj_, list):
            for i, v in enumerate(obj_):
                i_entry = str(i)
                _recursive_pydash_deep_paths(v, curr_path_ + (i_entry,), root_dict_)
        # Otherwise, we are at a base object, so just add this entry to the dict
        else:
            root_dict_[curr_path_] = obj_

    root_dict: dict[tuple[str, ...], str | int | float | bool | None] = {}
    _recursive_pydash_deep_paths(obj, tuple(), root_dict)

    # Join tuple-representation of the paths into deep string paths,
    # per https://pydash.readthedocs.io/en/stable/deeppath.html
    return {
        ".".join(k_i.replace(".", r"\.") for k_i in k): v for k, v in root_dict.items()
    }


def replace_template_variables(
    config: _JSON, replace_map: dict[str, _JSON], error_on_absence: bool = False
) -> _JSON:
    """Replace template variables in a JSON object with intended replacements.

    Only replaces template variables which are _values_ within the (nested) JSON
    object, not keys, etc.
    """
    # Work on copy
    config = pydash.clone_deep(config)

    # Generate a map of variable values to pydash-esque paths
    pydash_deep_paths = get_pydash_deep_paths(config)
    values_to_path_map = invert_dict(pydash_deep_paths)

    # Replace template values
    for replacement_key, replacement_value in replace_map.items():
        deep_paths = values_to_path_map.get(replacement_key)

        if deep_paths is None:
            err_str = f'No entry with value "{replacement_key}" found in passed object'
            if error_on_absence:
                raise ValueError(err_str)
            else:
                _logger.warning(err_str)
        else:
            for deep_path in deep_paths:
                # Sanity check that path already exists
                if pydash.has(config, deep_path):
                    pydash.set_(config, deep_path, replacement_value)
                else:
                    raise ValueError(
                        f'No deep path "{deep_path}" exists on passed object'
                    )

    return config


def replace_templated_variables(
    config_dict: dict[str, Any],
    template_params: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Replace templated variables in a task config.

    This function checks if a config has a 'template' section and automatically
    replaces template variables (like `{{ variable_name }}`) with ones supplied
    in the `template_params` argument. If not supplied, the default values
    from the template configuration are used instead.

    Args:
        config_dict: The configuration dictionary containing template variables
        template_params: Optional dictionary mapping template parameter names to values.
            These take precedence over default values.

    Returns:
        The configuration dictionary with template variables replaced by defaults

    Raises:
        ValueError: If a template variable has no default value and no template param
    """
    if "template" not in config_dict:
        return config_dict

    # Work on a copy to avoid modifying the original
    config = pydash.clone_deep(config_dict)

    # Extract template configuration
    template_config = config.pop("template")

    # Track which template_params were used
    used_template_params = set()

    # Process each template variable
    for variable_name, variable_info in template_config.items():
        # Create the template placeholder
        template_placeholder = f"{{{{ {variable_name} }}}}"

        # Priority 1: Use value from template_params if available
        if template_params and variable_name in template_params:
            replacement_value = template_params[variable_name]
            used_template_params.add(variable_name)
            _logger.info(
                f"Replacing template variable '{variable_name}' with value from "
                f"template_params: {replacement_value}"
            )
        else:
            # Priority 2: Use default value from template configuration
            default_value = variable_info.get("default")
            if default_value is None:
                raise ValueError(
                    f"Template variable '{variable_name}' has no default value and "
                    f"no template parameter was provided. Cannot replace template "
                    f"variable."
                )
            replacement_value = default_value
            _logger.info(
                f"Replacing template variable '{variable_name}' with default value: "
                f"{replacement_value}"
            )

        # Replace the template placeholder with the selected value
        config = _replace_template_value_recursive(
            config, template_placeholder, replacement_value
        )

    # Check for unused template_params and warn
    if template_params:
        unused_template_params = set(template_params.keys()) - used_template_params
        for unused_param in unused_template_params:
            _logger.warning(
                f"Template parameter '{unused_param}' was provided but not used "
                f"because no matching template variable was found"
            )

    return config


def _replace_template_value_recursive(
    obj: Any, template_placeholder: str, replacement_value: Any
) -> Any:
    """Recursively replace template placeholder in nested data structures."""
    if isinstance(obj, dict):
        return {
            key: _replace_template_value_recursive(
                value, template_placeholder, replacement_value
            )
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [
            _replace_template_value_recursive(
                item, template_placeholder, replacement_value
            )
            for item in obj
        ]
    elif isinstance(obj, str) and obj == template_placeholder:
        return replacement_value
    else:
        return obj
