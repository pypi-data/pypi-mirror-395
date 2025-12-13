"""Config YAML specification classes that are common to multiple other uses."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal, Optional, Union

import desert
from marshmallow import ValidationError, fields, validate
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union

from bitfount.data.datasplitters import PercentageSplitter, SplitterDefinedInData
from bitfount.runners.config_schemas.utils import (
    _deserialize_model_ref,
    _deserialize_path,
    keep_desert_output_as_dict,
)
from bitfount.types import _JSONDict

_DEFAULT_YAML_VERSION: Final[str] = "1.0.0"  # Default version is `1.0.0`
# so that unversioned yamls are still compatible with this version


@dataclass
class DataSplitConfig:
    """Configuration for the data splitter."""

    data_splitter: str = desert.field(
        fields.String(validate=OneOf(["percentage", "predefined"])),
        default="percentage",
    )
    # noinspection PyDataclass
    args: _JSONDict = desert.field(
        M_Union(
            [
                fields.Nested(
                    keep_desert_output_as_dict(desert.schema_class(PercentageSplitter))
                ),
                fields.Nested(
                    keep_desert_output_as_dict(
                        desert.schema_class(SplitterDefinedInData)
                    )
                ),
            ]
        ),
        default_factory=dict,
    )


class FilePath(fields.Field):
    """Field for representing file paths.

    Serializes to a string representation of the path and deserializes to a Python
    pathlib representation.
    """

    default_error_messages = {
        "invalid_path": 'Not a valid path; got "{invalid_type}"',
        "input_type": '"str" input type required, got "{input_type}"',
    }

    def _serialize(
        self, value: Any, attr: str | None, obj: Any, **kwargs: Any
    ) -> Optional[str]:
        """Take an Optional[Path] and convert to an absolute str-repr."""
        if value is None:
            return None
        if not isinstance(value, Path):
            raise self.make_error("invalid_path", invalid_type=str(type(value)))
        return str(value.expanduser().resolve())

    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Mapping[str, Any] | None,
        **kwargs: Any,
    ) -> Optional[Path]:
        """Take a str-repr path and convert to an absolute Path-repr.

        If context is not provided or doesn't contain "config_path", relative paths
        will be resolved relative to the current working directory.
        """
        if value is None:
            return None
        elif not isinstance(value, str):
            raise self.make_error("input_type", input_type=str(type(value)))
        else:
            # self.context is always a dict in marshmallow (defaults to {}), but
            # pass it explicitly to handle edge cases gracefully
            context = getattr(self, "context", None)
            return _deserialize_path(value, context)


class ModelReference(fields.Field):
    """Field for representing model references.

    If the reference is a path to a file (and that file exists), deserializes a Path
    instance. Otherwise, deserializes the str reference unchanged.

    Serializes both path and str to string.
    """

    default_error_messages = {
        "output_type": 'Not a valid "str" or path; got "{invalid_type}"',
        "input_type": '"str" input type required, got "{input_type}"',
    }

    def _serialize(
        self, value: Any, attr: str | None, obj: Any, **kwargs: Any
    ) -> Optional[str]:
        """Serialize a model reference.

        If the reference is a string, serialize to string.
        If the reference is a path, convert to an absolute str-repr.
        """
        if value is None:
            return None
        if not isinstance(value, (str, Path)):
            raise self.make_error("output_type", invalid_type=str(type(value)))
        if isinstance(value, str):
            return value
        else:
            return str(value.expanduser().resolve())

    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Mapping[str, Any] | None,
        **kwargs: Any,
    ) -> Optional[Union[Path, str]]:
        """Deserialize a model reference.

        If the model reference seems to be a file path (and that file exists)
        deserialize as a Path instance.
        Otherwise deserialize as a string.
        """
        if value is None:
            return None
        elif not isinstance(value, str):
            raise self.make_error("input_type", input_type=str(type(value)))
        else:
            return _deserialize_model_ref(value)


class TemplatedOrTyped(fields.Field):
    """A field that accepts either a templated string or the expected type.

    This field allows YAML validation to pass for both templated strings
    (like `{{ variable_name }}`) and the actual expected type, helping
    with YAML linting for template files.

    The templated string must match the pattern: `{{ variable_name }}`
    """

    # Regex pattern for template variables: {{ variable_name }}
    TEMPLATE_PATTERN = r"^\{\{\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\}\}$"

    def __init__(self, inner_field: fields.Field, **kwargs: Any):
        """Initialize with the inner field type.

        Args:
            inner_field: The actual field type expected when not templated
            **kwargs: Additional keyword arguments passed to parent
        """
        # Inherit allow_none from inner field if not explicitly set
        if "allow_none" not in kwargs and hasattr(inner_field, "allow_none"):
            kwargs["allow_none"] = inner_field.allow_none
        super().__init__(**kwargs)
        self.inner_field = inner_field

    def _serialize(
        self, value: Any, attr: Optional[str], obj: Any, **kwargs: Any
    ) -> Any:
        """Serialize the value."""
        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
            return value
        return self.inner_field._serialize(value, attr, obj, **kwargs)

    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        """Deserialize the value."""
        # If it's a templated string, validate pattern and return as-is
        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
            import re

            if not re.match(self.TEMPLATE_PATTERN, value):
                raise ValidationError(
                    f"Template string must match pattern {{{{ variable_name }}}}, got: {value}"  # noqa: E501
                )
            return value
        # Otherwise, deserialize using the inner field
        return self.inner_field.deserialize(value, attr, data)


@dataclass
class PathConfig:
    """Configuration for the path."""

    path: Path = desert.field(FilePath())


SecretsUse = Literal["bitfount", "ehr"]


@dataclass
class TemplatedGroupingConfig:
    """Configuration for grouping files into cohorts for processing."""

    group_by: list[str] | None = desert.field(
        TemplatedOrTyped(fields.List(fields.String())),
    )
    order_by: list[tuple[str, str]] | None = desert.field(
        TemplatedOrTyped(
            fields.List(
                fields.Tuple(
                    (
                        fields.String(),
                        fields.String(validate=validate.OneOf(["asc", "desc"])),
                    )
                ),
                allow_none=True,
            )
        ),
        default=None,
    )
    per_group_head: dict[str, int] | None = desert.field(
        TemplatedOrTyped(
            fields.Dict(keys=fields.String(), values=fields.Integer(), allow_none=True)
        ),
        default=None,
    )

    include_non_new_group_files: bool = True
