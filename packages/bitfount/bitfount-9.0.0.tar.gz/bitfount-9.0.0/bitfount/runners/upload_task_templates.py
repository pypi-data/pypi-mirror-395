r"""This script takes a config of task templates and uploads them to bitfount hub.

The config also contains paths to any custom models and weights that are used in the
task templates. If the models or weights have changed since the last upload, the models
and weights are uploaded to bitfount hub and the task templates are updated to use the
new versions of the models and weights. Finally, there is also the option to archive
task templates that are no longer used.
```

Example dev usage:

```bash
BITFOUNT_ENVIRONMENT=dev python -m bitfount.runners.upload_task_templates \\
task_templates/config-staging-public.yaml -u <username>
```

Example production usage:

```bash
python -m bitfount.runners.upload_task_templates \\
task_templates/config-production-public.yaml -u <username>
```

The above command can also be run with the `--password` flag to provide the password
for the user. If the password is not provided, an authentication flow will be started.
"""

from datetime import datetime, timedelta, timezone
import logging
import os
from pathlib import Path
import re
from typing import Any, Literal, Optional, Union, cast
from warnings import warn

from fire import Fire
from pydantic import BaseModel, ValidationError
from requests import HTTPError
import yaml

from bitfount import BitfountModelReference
from bitfount.externals.general.authentication import ExternallyManagedJWT
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.helper import _create_bitfounthub, get_hub_url
from bitfount.hub.utils import hash_file_contents
from bitfount.runners.config_schemas.hub_schemas import APIKeys
from bitfount.types import BaseModelProtocol, _StrAnyDict
from bitfount.utils.web_utils import post

BF_USER_PUBLIC_TASKS = "bitfount"
BF_USER_PRIVATE_TASKS = "bitfount-tasks"

AUTH0_AUDIENCE = "https://hub.bitfount.com/api"
AUTH0_TOKEN_URL_FORMAT = "https://{auth_domain}/oauth/token"  # nosec
AUTH0_REALM_DEV = "Username-Password-Authentication"
AUTH0_REALM_PROD = "bitfount-db"


# If being run as a script, make sure that the logging takes place under the bitfount
# logging namespace
if __name__ != "__main__":
    _logger = logging.getLogger(__name__)
else:
    _logger = logging.getLogger("bitfount")


def get_username_to_use(config_file: os.PathLike) -> str:
    """Gets the username to use for the task template owner."""
    if "public" in str(config_file):
        return BF_USER_PUBLIC_TASKS
    else:
        return BF_USER_PRIVATE_TASKS


class ModelConfig(BaseModel):
    """Model config model for static and runtime type checking."""

    model_file: str
    private: bool = True
    weights_file: Optional[str] = None


class BasicTaskTemplateConfig(BaseModel):
    """Base task template config model for static and runtime type checking."""

    slug: str


class TaskTemplateConfig(BasicTaskTemplateConfig):
    """Model config model for static and runtime type checking."""

    title: str
    type: (
        Literal["image-segmentation"]
        | Literal["image-classification"]
        | Literal["object-detection"]
        | Literal["text-classification"]
        | Literal["text-generation"]
        | Literal["tabular-classification"]
        | Literal["tabular-regression"]
        | Literal["tabular-analytics"]
        | Literal["data-transfer"]
    )
    description: str
    template: str
    tags: list[
        (
            Literal["Prediction"]
            | Literal["Training"]
            | Literal["Evaluation"]
            | Literal["Querying"]
            | Literal["Comparison"]
            | Literal["Ophthalmology"]
            | Literal["File Selection"]
        )
    ]
    sampleDatasetDownloadUrl: Optional[str] = None


def main(
    config_file: os.PathLike,
    password: Optional[str] = None,
    username: Optional[str] = None,
) -> None:
    """Uploads models, weights and task templates to bitfount.

    Iterates over the models in the config file and uploads them to bitfount if
    the code hash or weights are different from the latest version on bitfount.
    Once the models are updated, the task templates are updated to use the latest
    versions of the models and the task templates are themselves uploaded to bitfount.

    Args:
        config_file: The path to the YAML config.
        username: The username for the task template owner. Defaults to
            None and gets set based on config used.
        password: The password for the task template owner.
    """
    config_file = Path(str(config_file).lower())
    if not username:
        username = get_username_to_use(config_file)
    with open(config_file, "r") as f:
        config_yaml = yaml.safe_load(f)

    if not config_yaml:
        _logger.info("Config file is empty, returning early")
        return

    jwt = _get_jwt(username, password)
    model_names_and_versions = {}

    if "models" in config_yaml:
        _logger.info("Uploading models")
        model_names_and_versions = _get_model_names_and_versions(
            config_yaml, username, jwt=jwt, upload_models=True
        )

    if "task-templates" in config_yaml:
        _logger.info("Uploading task templates")
        update_and_upload_task_templates(
            config_yaml, username, model_names_and_versions, jwt=jwt
        )

    if "deprecated-task-templates" in config_yaml:
        _logger.info("Archiving old templates")
        _archive_templates(config_yaml, username, jwt=jwt)


def _get_jwt(
    username: str,
    password: Optional[str] = None,
) -> Optional[ExternallyManagedJWT]:
    """Gets a JWT for the user if the password is provided.

    Args:
        username: The username for the user.
        password: The password for the user.

    Returns:
        A JWT for the user or None if pwd not provided.
    """
    jwt = None
    if password is not None:
        print("Using JWT for authentication")
        access_token, expires_in = _get_user_token(username, password)
        jwt = ExternallyManagedJWT(
            jwt=access_token,
            expires=datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            # Refreshing not necessary as this is not a long-running script
            get_token=lambda: None,  # type: ignore[arg-type, return-value]
        )
    return jwt


def _archive_templates(
    config_yaml: _StrAnyDict, username: str, jwt: Optional[ExternallyManagedJWT] = None
) -> None:
    """Archive task templates that are no longer used.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        jwt: The JWT for the model owner.

    Raises:
        ValueError: If the task template config is invalid.
    """
    hub_url = get_hub_url()
    task_template_url = f"{hub_url}/api/task-templates/{username}"
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)
    for template in config_yaml["deprecated-task-templates"]:
        # Validate the task template config. If it is invalid, raise an error
        try:
            validated_template = BasicTaskTemplateConfig(**template)
        except ValidationError as e:
            raise ValueError(f"Invalid task template config: {e}") from e

        _logger.info(f"Archiving task template: {validated_template.slug}")
        archive_template_response = hub.session.patch(
            url=f"{task_template_url}/{validated_template.slug}",
            data={"state": "archived"},
        )

        try:
            archive_template_response.raise_for_status()
        except HTTPError:
            _logger.error(vars(archive_template_response))
        else:
            _logger.info(f"Task template {validated_template.slug} archived.")


def _unarchive_template(
    template: BasicTaskTemplateConfig,
    username: str,
    jwt: Optional[ExternallyManagedJWT] = None,
) -> None:
    """Unarchive task templates that were previously archived.

    This must be done via the PATCH method, the POST method will not work.

    Args:
        template: The config yaml.
        username: The username for the model owner.
        jwt: The JWT for the model owner.
    """
    hub_url = get_hub_url()
    task_template_url = f"{hub_url}/api/task-templates/{username}"
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)
    _logger.info(f"Unarchiving task template: {template.slug}")
    archive_template_response = hub.session.patch(
        url=f"{task_template_url}/{template.slug}",
        data={"state": "published"},
    )

    try:
        archive_template_response.raise_for_status()
    except HTTPError:
        _logger.error(vars(archive_template_response))
    else:
        _logger.info(f"Task template {template.slug} unarchived.")


def _get_model_names_and_versions(
    config_yaml: _StrAnyDict,
    username: str,
    jwt: Optional[ExternallyManagedJWT] = None,
    upload_models: bool = False,
) -> dict[str, int]:
    """Gets the model names and versions from the config file.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        jwt: The JWT for the model owner.
        upload_models: Whether to upload the models to bitfount hub if they are not
            already present on bitfount hub or if the hashes or weights are different
            from the latest version on bitfount. If False, the function will return
            only the model names and latest versions that are present on bitfount hub.

    Returns:
        A dictionary containing the model names and new version numbers.

    Raises:
        ValueError: If the model config is invalid.
    """
    model_names_and_versions: dict[str, int] = {}
    hub_url = get_hub_url()
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)

    # Iterate over the models in the config file
    for model_config in config_yaml["models"]:
        # Validate the model config. If it is invalid, raise an error
        try:
            validated_model_config = ModelConfig(**model_config)
        except ValidationError as e:
            raise ValueError(f"Invalid model config: {e}") from e

        _logger.info(f"Will upload model {validated_model_config}")

        model_name_from_path = Path(validated_model_config.model_file).stem
        try:
            model_ref = BitfountModelReference(
                model_ref=model_name_from_path,
                username=username,
                secrets=jwt,
                hub=hub,
            )
        except ValueError as e:
            # Handles when _get_model_version_from_hub fails with
            # ValueError because model is not yet uploaded to the hub.
            missing_msg = "was not found on the Bitfount Hub"
            if missing_msg in str(e):
                model_response = None
                _logger.debug(
                    f"Model {model_name_from_path} not yet on hub; will treat as new."
                )
            else:
                raise
        else:
            model_response = model_ref.hub._get_model_response(
                username=username,
                model_name=cast(str, model_ref.model_ref),
            )

        # If the model is not present on bitfount, upload it
        if model_response is None and upload_models:
            _upload_model_and_weights(validated_model_config, username, secrets=jwt)
            # TODO: [BIT-3129] ensure that the first version is always 1
            #  (can be 0 at the moment)
            model_names_and_versions[model_name_from_path] = 1
        # If the model is present on bitfount, check if the code hash or weights
        # are different from the latest version on bitfount and upload to a new
        # version if they are different
        elif model_response is None and not upload_models:
            _logger.warning(
                f"Model {validated_model_config.model_file} is not present on bitfount",
                "hub but upload_models is False, so will not upload.",
            )
        elif model_response is not None:
            model_version = model_response["modelVersion"]
            hub_model_hash = model_response["modelHash"]
            model_hash = hash_file_contents(Path(validated_model_config.model_file))
            hashes_different = hub_model_hash != model_hash
            weights_different = False
            if validated_model_config.weights_file is not None and upload_models:
                try:
                    hub_model_weights = model_ref.hub.get_weights(
                        username=username,
                        model_name=cast(str, model_ref.model_ref),
                        model_version=model_version,
                    )
                except HTTPError as e:
                    _logger.warning(
                        f"Could not get weights from S3: {e.strerror}\n"
                        f"Will continue assuming there are no weights defined"
                    )
                    hub_model_weights = None
                model_weights = Path(validated_model_config.weights_file).read_bytes()
                weights_different = hub_model_weights != model_weights
            if (hashes_different or weights_different) and upload_models:
                _upload_model_and_weights(validated_model_config, username, secrets=jwt)
                model_names_and_versions[cast(str, model_ref.model_ref)] = (
                    model_version + 1
                )
            else:
                _logger.info(
                    f"Model {validated_model_config.model_file} is already up to date."
                )
                model_names_and_versions[cast(str, model_ref.model_ref)] = model_version
    return model_names_and_versions


def update_and_upload_task_templates(
    config_yaml: _StrAnyDict,
    username: str,
    model_names_and_versions: dict[str, int],
    jwt: Optional[ExternallyManagedJWT] = None,
    keep_slug: bool = False,
    testing: bool = False,
) -> Union[list[_StrAnyDict], dict[str, _StrAnyDict]]:
    """Updates the task templates and uploads them to bitfount hub if they have changed.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        model_names_and_versions: A dictionary containing the model names and new
            version numbers.
        jwt: The JWT for the model owner.
        keep_slug: Whether to return the task templates with the slug as the key.
        testing: Used to indicate whether this function is used in a testing context.
            If True, the function will not make any requests to the hub.

    Raises:
        ValueError: If the task template config is invalid.
    """
    hub_url = get_hub_url()
    task_template_url = f"{hub_url}/api/task-templates"
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)
    task_templates_with_slug: dict[str, _StrAnyDict] = {}
    task_templates: list[_StrAnyDict] = []
    for task_template_config in config_yaml["task-templates"]:
        # Validate the task template config. If it is invalid, raise an error
        try:
            validated_task_template_config = TaskTemplateConfig(**task_template_config)
        except ValidationError as e:
            raise ValueError(f"Invalid task template config: {e}") from e

        # Update the model version on task templates that reference any models whose
        # version has changed
        with open(validated_task_template_config.template, "r") as f:
            template = yaml.safe_load(f)

        template = _add_username_to_yaml_config(template, username)

        # If model files are provided, we will have model_names_and_versions,
        # and can update the references in the YAML. Otherwise, don't update.
        if model_names_and_versions:
            template = _update_yaml_config(template, model_names_and_versions, username)
        else:
            _logger.info(
                "No models provided to upload, will assume references are valid."
            )

        slug = _sanitise_task_template_slug(validated_task_template_config.slug)
        _logger.info(f"Parsing task template: {slug}")

        task_template = {
            "title": validated_task_template_config.title,
            "slug": slug,
            "type": validated_task_template_config.type,
            "template": template,
            "description": validated_task_template_config.description,
            "tags": validated_task_template_config.tags,
        }

        # Check if a task template already exists for this user & slug.
        task_template_slug_url = f"{task_template_url}/{username}/{slug}"
        if not testing:
            template_exists_response = hub.session.get(url=task_template_slug_url)
            if template_exists_response.status_code == 200:
                task_template_on_hub = template_exists_response.json()

                # If the task template is archived, un-archive it before
                # updating the content
                if task_template_on_hub["state"] == "archived":
                    _unarchive_template(
                        validated_task_template_config, username, jwt=jwt
                    )

                # If the tags are changed, then update
                # template without creating a new version
                if (template == task_template_on_hub["template"]) and (
                    validated_task_template_config.tags != task_template_on_hub["tags"]
                ):
                    _logger.info(f'Task "{slug}" has new tags. Updating tags.')
                    template_update_body = {
                        "tags": validated_task_template_config.tags,
                    }
                    template_update_response = hub.session.patch(
                        url=task_template_slug_url,
                        json=template_update_body,
                    )

                    try:
                        template_update_response.raise_for_status()
                    except HTTPError as e:
                        response_body = template_update_response.text
                        raise HTTPError(
                            f"Task template upload failed with error: {e}. "
                            f"Template upload response body: {response_body}",
                            response=template_update_response,
                        ) from e
                # If the sampleDatasetDownloadUrl is changed, then update
                # template without creating a new version
                if (template == task_template_on_hub["template"]) and (
                    validated_task_template_config.sampleDatasetDownloadUrl
                    != task_template_on_hub.get("sampleDatasetDownloadUrl", None)
                ):
                    _logger.info(
                        f'Task "{slug}" has a new sample dataset url. Updating the url.'
                    )
                    sample_url: Optional[str] = (
                        validated_task_template_config.sampleDatasetDownloadUrl
                    )
                    url_update_body = {
                        "sampleDatasetDownloadUrl": sample_url,
                    }
                    template_update_response = hub.session.patch(
                        url=task_template_slug_url,
                        json=url_update_body,
                    )

                    try:
                        template_update_response.raise_for_status()
                    except HTTPError as e:
                        response_body = template_update_response.text
                        raise HTTPError(
                            f"Task template upload failed with error: {e}. "
                            f"Template upload response body: {response_body}",
                            response=template_update_response,
                        ) from e

                if (template == task_template_on_hub["template"]) and (
                    validated_task_template_config.description
                    == task_template_on_hub["description"]
                ):
                    # If the task template or the description have not changed
                    # then we will skip updating this template
                    _logger.info(
                        f'Task "{slug}" is unchanged, not creating new version.'
                    )
                    task_templates.append(template)
                    task_templates_with_slug[slug] = template

                    continue

                _logger.info(f"Updating task template: {slug}")
                # If the template already exists, push a new version to the hub
                template_upload_response = hub.session.post(
                    url=task_template_slug_url,
                    json=task_template,
                )
            else:
                _logger.info(f"Creating task template: {slug}")
                # If the template does not exist, create a new task template by POSTing
                # to a different endpoint
                template_upload_response = hub.session.post(
                    url=task_template_url,
                    json=task_template,
                )

            try:
                template_upload_response.raise_for_status()
            except HTTPError as e:
                response_body = template_upload_response.text
                raise HTTPError(
                    f"Task template upload failed with error: {e}. "
                    f"Template upload response body: {response_body}",
                    response=template_upload_response,
                ) from e
        task_templates_with_slug[slug] = template
        task_templates.append(template)
    if keep_slug:
        return task_templates_with_slug
    else:
        return task_templates


def _sanitise_task_template_slug(slug: str) -> str:
    """Ensure provided slug is valid and sanitised.

    Args:
        slug: The slug to sanitise.

    Returns:
        The sanitised slug.
    """
    # Slug name sanitisation
    # Needs to be only alphanumeric characters
    alpha_safe_slug = re.sub(r"[^0-9a-z]", "-", slug.strip().lower())
    # No consecutive hyphens
    double_hyphen_safe_slug = re.sub(r"(-)+", "-", alpha_safe_slug)
    # No hyphens at the start or end
    external_hyphen_safe_slug = re.sub(r"^-|-$", "", double_hyphen_safe_slug)
    # Less than 50 characters
    slug = external_hyphen_safe_slug[:50]
    return slug


def _update_yaml_config(
    config_yaml: _StrAnyDict, model_names_and_versions: dict[str, int], username: str
) -> _StrAnyDict:
    """Update the model version in the yaml config.

    Args:
        config_yaml: The yaml config.
        model_names_and_versions: A dictionary containing the model names and new
            version numbers.
        username: The username for the model owner.

    Returns:
        The updated yaml config.

    Raises:
        ValueError: If the model is not found in the config.
    """
    for index, algo_config in enumerate(config_yaml["task"]["algorithm"]):
        if "model" in algo_config and "bitfount_model" in algo_config["model"]:
            updated_model_version = False
            # If the model is a bitfount model, iterate over new model versions
            # to find a match and update the version number
            for model_slug, model_version in model_names_and_versions.items():
                if algo_config["model"]["bitfount_model"]["model_ref"] == model_slug:
                    config_yaml["task"]["algorithm"][index]["model"]["bitfount_model"][
                        "model_version"
                    ] = model_version
                    config_yaml["task"]["algorithm"][index]["model"]["bitfount_model"][
                        "username"
                    ] = username
                    updated_model_version = True
                    break
            if not updated_model_version:
                # This is a warning rather than an exception to allow for the uploading
                # of task templates that reference models that are not in the config
                # e.g. a model belonging to another user
                warn(
                    f"Model {algo_config['model']['bitfount_model']['model_ref']} "
                    "was not referenced in the model config."
                )

    return config_yaml


def _get_user_token(
    username: str,
    password: str,
) -> tuple[str, int]:
    """Gets a user token from auth0 to use for authentication.

    Args:
        username: The username to authenticate with.
        password: The password to authenticate with.

    Returns:
        A tuple containing the access token and length in seconds until the token
        expires.
    """
    auth_environment = _get_auth_environment()
    realm = (
        AUTH0_REALM_DEV if auth_environment.name == "development" else AUTH0_REALM_PROD
    )

    token_url = AUTH0_TOKEN_URL_FORMAT.format(auth_domain=auth_environment.auth_domain)

    token_response = post(
        token_url,
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": username,
            "password": password,
            "audience": AUTH0_AUDIENCE,
            "client_id": auth_environment.client_id,
            "scope": "profile",
            "realm": realm,
        },
        timeout=10,
    )
    token_response_json = token_response.json()
    try:
        return token_response_json["access_token"], token_response_json["expires_in"]
    except KeyError:
        _logger.critical(
            f"Unable to retrieve details from JWT. JSON was: {token_response_json}"
        )
        raise


def _add_username_to_yaml_config(
    config_yaml: _StrAnyDict, username: str
) -> dict[str, Any]:
    """Adds the username to the config.

    If the username is not present in the custom model config, the specified username
    is added to the config instead.

    Args:
        config_yaml: The yaml config.
        username: The username for the model owner.

    Returns:
        The updated yaml config.
    """
    if not isinstance(config_yaml["task"]["algorithm"], list):
        config_yaml["task"]["algorithm"] = [config_yaml["task"]["algorithm"]]
    for algo in config_yaml["task"]["algorithm"]:
        if (
            "model" in algo
            and "bitfount_model" in algo["model"]
            and "username" not in algo["model"]["bitfount_model"]
        ):
            algo["model"]["bitfount_model"]["username"] = username
    return config_yaml


def _upload_model_and_weights(
    model_config: ModelConfig,
    username: str,
    secrets: Optional[Union[APIKeys, ExternallyManagedJWT]] = None,
) -> None:
    """Uploads the model and weights to bitfount hub.

    Before uploading the model, it is checked that the model implements
    BaseDistributedModelProtocol.

    Args:
        model_config: The model config to upload.
        username: The username for the model owner.
        secrets: The secrets for the model owner.

    Raises:
        TypeError: If the model does not implement BaseDistributedModelProtocol.
        ValueError: If model upload fails.
    """
    model_ref = BitfountModelReference(
        model_ref=Path(model_config.model_file),
        private=model_config.private,
        username=username,
        secrets=secrets,
    )
    model_cls = model_ref._get_model_from_path()

    try:
        assert issubclass(model_cls, BaseModelProtocol)  # nosec[assert_used]
    except AssertionError as e:
        raise TypeError(
            f"Model {model_config.model_file} must implement BaseModelProtocol."
        ) from e
    upload_response = model_ref._upload_model_to_hub()  # uploads the model
    if upload_response is None:
        raise ValueError("Model upload failed.")
    model_version = upload_response["version"]
    model_ref.model_version = model_version
    if model_config.weights_file is not None:
        # uploads the weights
        model_ref.send_weights(Path(model_config.weights_file))


if __name__ == "__main__":
    Fire(main)
