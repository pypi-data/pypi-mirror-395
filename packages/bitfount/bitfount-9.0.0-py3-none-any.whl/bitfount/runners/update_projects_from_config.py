#!/usr/bin/env python3
r"""Script to update projects from a configuration file.

This script reads a config file containing project IDs, task template slugs,
and variables, then ensures each project is updated with the correct task
template version and configurable variables.

Example usage:
    python -m bitfount.runners.update_projects_from_config \\
    task_templates/project-config-production-public.yaml --username myuser \\
    --password mypass
"""

from datetime import datetime, timedelta, timezone
from enum import Enum
import json
import os
from pathlib import Path
import sys
import traceback
from typing import Any, Literal, Optional, cast

from fire import Fire
import pydash
from requests import Response
import yaml

from bitfount.externals.general.authentication import ExternallyManagedJWT
from bitfount.hub.api import BitfountHub
from bitfount.hub.helper import _create_bitfounthub, get_hub_url
from bitfount.runners.upload_task_templates import (
    _get_user_token,
    update_and_upload_task_templates,
)

# Type aliases
# Project: {
#   id?: string;
#   /** Format: date-time */
#   created_at?: string;
#   /** Format: date-time */
#   updated_at?: string;
#   name: string;
#   role?: components["schemas"]["ProjectRole"];
#   metadata: Record<string, unknown>;
#   linked_datasets?: components["schemas"]["LinkedDataset"][];
#   linked_datasets_count?: number;
#   status?: components["schemas"]["ProjectStatus"];
#   tags?: string[];
#   isDemo?: boolean;
#   imageUrl?: string;
# };
ProjectInfo = dict[str, Any]
# PaginatedResponse: {
#   results: TaskDefinition[];
#   total: number;
#   offset?: number;
# };
# TaskDefinition: {
#   /** Format: uuid */
#   id: string;
#   name: string;
#   description: string;
#   definition: components["schemas"]["UserSubmittedTaskDefinition"];
#   /** Format: uuid */
#   projectId: string;
#   /** Format: date-time */
#   createdAt: string;
#   /** Format: date-time */
#   updatedAt: string;
#   taskTemplateSummary?: components["schemas"]["TaskTemplateSummary"];
#   referencedModels?: components["schemas"]["ModelReference"][];
# };
ProjectTaskDefinitions = dict[str, Any]
# For one single entry of ProjectTaskDefinitions["results"]
TaskDefinition = dict[str, Any]
# TaskTemplateWithModels: {
#   /** Format: uuid */
#   id: string;
#   ownerUsername: string;
#   slug: string;
#   version: number;
#   title: string;
#   /** Format: date-time */
#   createdAt: string;
#   /** Format: date-time */
#   updatedAt: string;
#   "type": string;
#   template: Record<string, unknown>;
#   description: string;
#   state: components["schemas"]["TaskTemplateState"];
#   tags?: components["schemas"]["TaskTemplateTags"][];
#   sampleDatasetDownloadUrl?: string;
#   models: components["schemas"]["ModelReference"][];
# };
TaskTemplateInfo = dict[str, Any]


# These are the paths to the config files of task templates. They are used to find the
# local task template file from the slug of the task template.
TASK_TEMPLATES_CONFIG_PATHS: list[str] = [
    "task_templates/config-production-hidden.yaml",
    "task_templates/config-production-public.yaml",
]

# What type to use for the new variables. Defaults to "fixed". The other option is
# "default".
TASK_VARIABLE_MODE = "fixed"

TaskTemplateVersionOptions = Literal[
    # Tries to update the task template to the latest version, failing if the task
    # templates are outdated
    "latest",
    # Does not try to update the task template at all (though still will apply
    # template variable updates), simply checks that _a_ version of that task
    # template exists. This will result in the project configuration sticking
    # with the task template version that it was created with.
    "project-current",
    # If the project’s task template is not the same as the SDK version then skip
    # updating the project. If it is the same, then update the templated variables.
    "sdk-skip",
    # Same as sdk-skip but instead will fail the job if the versions differ. If it is
    # the same, then update the templated variables.
    "sdk-fail",
]


class SkipProjectException(Exception):
    """Skip updating this project."""

    pass


class FailProjectException(Exception):
    """Fail updating this project."""

    pass


class ProcessResult(Enum):
    """Enum representing the result of processing a project."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class ProjectConfig:
    """Class to represent a project configuration."""

    def __init__(self, project_id: str, config_data: dict[str, Any]):
        self.project_id = project_id
        task_slug_full = config_data["task-slug"]

        # Parse the owner and slug from the format "owner/slug"
        if "/" not in task_slug_full:
            raise ValueError(
                f"Task slug must be in format 'owner/slug', got: {task_slug_full}"
            )

        self.task_owner, self.task_slug = task_slug_full.split("/", 1)
        self.task_template_version: int | TaskTemplateVersionOptions = config_data.get(
            "task-template-version", "latest"
        )
        self.project_owner = config_data["project-owner"]
        self.variables = config_data.get("variables", {})


def load_config(config_file: str) -> list[ProjectConfig]:
    """Load and parse the project configuration file.

    Args:
        config_file: Path to the YAML configuration file.

    Returns:
        List of ProjectConfig objects.
    """
    print(f"📄 Loading config file: {config_file}")
    print(f"📍 File exists: {os.path.exists(config_file)}")
    with open(config_file, "r") as f:
        config_data = yaml.safe_load(f)

    projects = []
    for project_entry in config_data.get("project_ids", []):
        for project_id, project_config in project_entry.items():
            projects.append(ProjectConfig(project_id, project_config))

    return projects


def _get_project_info(project_id: str, hub: BitfountHub, hub_url: str) -> Response:
    """Get current project information from the hub."""
    project_url: str = f"{hub_url}/api/projects/{project_id}"
    response = hub.session.get(url=project_url)
    return response


def get_project_info(
    project_id: str,
    hub: BitfountHub,
    hub_url: str,
) -> ProjectInfo:
    """Get current project information from the hub.

    Args:
        project_id: The project ID to retrieve.
        hub: The hub connection object.
        hub_url: The hub URL.

    Returns:
        Project information dictionary or None if not found.

    Raises:
        FailProjectException: If the project could not be found or accessed.
    """
    try:
        response = _get_project_info(project_id, hub, hub_url)
        if response.status_code == 200:
            return cast(ProjectInfo, response.json())
        elif response.status_code == 404:
            print(f"❌ Project not found: {project_id}")
            raise FailProjectException("Project not found")
        elif response.status_code == 403:
            print(f"❌ Access denied to project: {project_id}")
            raise FailProjectException("Access denied to project")
        else:
            print(f"❌ Failed to get project {project_id}: {response.status_code}")
            raise FailProjectException("Failed to get project")
    except Exception as e:
        print(f"❌ Error getting project {project_id}: {e}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        if isinstance(e, FailProjectException):
            # If the exception is a FailProjectException, re-raise it as-is to avoid
            # losing the original context
            raise
        else:
            raise FailProjectException(f"Error getting project: {e}") from e


def _get_project_task_definitions(
    project_id: str, hub: BitfountHub, hub_url: str
) -> Response:
    """Get task definitions for a project from the hub."""
    definitions_url: str = f"{hub_url}/api/projects/{project_id}/task-definitions"
    response = hub.session.get(url=definitions_url)
    return response


def get_project_task_definitions(
    project_id: str, hub: BitfountHub, hub_url: str
) -> ProjectTaskDefinitions:
    """Get task definitions for a project from the hub.

    Args:
        project_id: The project ID.
        hub: The hub connection object.
        hub_url: The hub URL.

    Returns:
        Task definitions response dictionary or None if not found.

    Raises:
        FailProjectException: If the task definitions could not be found or accessed.
    """

    try:
        response = _get_project_task_definitions(project_id, hub, hub_url)
        if response.status_code == 200:
            return cast(ProjectTaskDefinitions, response.json())
        elif response.status_code == 404:
            print(f"❌ Task definitions not found for project: {project_id}")
            raise FailProjectException("Task definitions not found")
        elif response.status_code == 403:
            print(f"❌ Access denied to task definitions for project: {project_id}")
            raise FailProjectException("Access denied to task definitions")
        else:
            print(
                f"❌ Failed to get task definitions for project {project_id}: "
                f"{response.status_code}"
            )
            raise FailProjectException("Failed to get task definitions for project")
    except Exception as e:
        print(f"❌ Error getting task definitions for project {project_id}: {e}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        if isinstance(e, FailProjectException):
            # If the exception is a FailProjectException, re-raise it as-is to avoid
            # losing the original context
            raise
        else:
            raise FailProjectException(
                f"Error getting task definitions for project: {e}"
            ) from e


def get_latest_task_definition_for_project(
    project_id: str, hub: BitfountHub, hub_url: str
) -> Optional[TaskDefinition]:
    """Gets the latest task definition for a project from the hub.

    Returns `None` if there is no task definition.
    """
    task_definitions_response = get_project_task_definitions(project_id, hub, hub_url)
    latest_task_def: Optional[TaskDefinition] = pydash.get(
        task_definitions_response, "results.[-1]"
    )
    return latest_task_def


def _get_task_template_info(hub: BitfountHub, template_url: str) -> Response:
    """Get task template information from the hub."""
    response = hub.session.get(url=template_url)
    return response


def get_task_template_info(
    owner_or_id: str,
    slug: Optional[str],
    hub: BitfountHub,
    hub_url: str,
) -> TaskTemplateInfo:
    """Get task template information from the hub by owner/slug or by ID.

    Gets the latest task template for a given owner/slug, gets the specific version
    if provided with ID.

    Args:
        owner_or_id: Either the task template owner (if slug provided) or template ID.
        slug: The task template slug (if getting by owner/slug), None if getting by ID.
        hub: The hub connection object.
        hub_url: The hub URL.

    Returns:
        Task template information dictionary or None if not found.
    """
    if slug:
        # Get by owner/slug
        template_url: str = f"{hub_url}/api/task-templates/{owner_or_id}/{slug}"
        identifier = f"{owner_or_id}/{slug}"
    else:
        # Get by ID
        template_url = f"{hub_url}/api/task-templates/{owner_or_id}"
        identifier = f"ID {owner_or_id}"

    try:
        response = _get_task_template_info(hub, template_url)
        if response.status_code == 200:
            return cast(TaskTemplateInfo, response.json())
        elif response.status_code == 404:
            print(f"❌ Task template not found: {identifier}")
            raise FailProjectException("Task template not found")
        else:
            print(
                f"❌ Failed to get task template {identifier}: {response.status_code}"
            )
            raise FailProjectException("Failed to get task template")
    except Exception as e:
        print(f"❌ Error getting task template {identifier}: {e}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        if isinstance(e, FailProjectException):
            # If the exception is a FailProjectException, re-raise it as-is to avoid
            # losing the original context
            raise
        else:
            raise FailProjectException(f"Error getting task template: {e}") from e


def get_or_update_latest_task_template(
    project_config: ProjectConfig,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> str:
    """Check if task template on hub is the latest version and update if necessary.

    Args:
        project_config: The project configuration.
        username: The authenticated username.
        jwt: The JWT token.
        hub: The hub connection object.
        hub_url: The hub URL.

    Returns:
        The task template ID to use, corresponding to the latest version of the task
        template.

    Raises:
        SkipProjectException: If project should be skipped.
        FailProjectException: If project update should be failed.
    """
    # Use the task owner and slug directly from the config
    task_owner = project_config.task_owner
    task_slug = project_config.task_slug

    print(f"📋 Using task template '{task_slug}' owned by '{task_owner}'")

    # Get full task template info to validate it exists
    latest_hub_task_template_info: Optional[TaskTemplateInfo] = get_task_template_info(
        task_owner, task_slug, hub, hub_url
    )

    if not latest_hub_task_template_info:
        print(f"❌ Cannot find task template '{task_owner}/{task_slug}'")
        raise FailProjectException("Task template not found")

    template_id: Optional[str] = latest_hub_task_template_info.get("id")
    if not template_id:
        print(f"❌ Task template '{task_owner}/{task_slug}' has no ID")
        raise FailProjectException("Task template ID not found")

    # Parse the task templates config to find the template file path
    local_task_template_path = _find_local_task_template_by_slug(task_slug)
    if not local_task_template_path:
        print(
            f"⚠️  Task template slug '{task_slug}' not found in any config files: {TASK_TEMPLATES_CONFIG_PATHS}"  # noqa: E501
        )
        print("ℹ️  Using hub version")
        return template_id

    if not Path(local_task_template_path).exists():
        print(f"⚠️  Local template file not found: {local_task_template_path}")
        print("ℹ️  Using hub version")
        return template_id

    # Found local template file and it exists
    print(f"📄 Found local template file: {local_task_template_path}")

    # Load local template
    with open(local_task_template_path, "r") as f:
        local_template: dict[str, Any] = yaml.safe_load(f)

    # Compare with hub template
    hub_template: dict[str, Any] = latest_hub_task_template_info.get("template", {})

    # Sort both templates recursively to avoid false positives due to key ordering
    sorted_local_template = _sort_dict_recursively(local_template)
    sorted_hub_template = _sort_dict_recursively(hub_template)

    if sorted_local_template != sorted_hub_template:
        # Check if the authenticated user owns the task template
        if username != task_owner:
            print(
                f"⚠️  Task template '{task_owner}/{task_slug}' is not "
                f"up to date and is owned by '{task_owner}', not "
                f"authenticated user '{username}'. Skipping entire project."
            )
            _print_template_differences(sorted_local_template, sorted_hub_template)
            raise SkipProjectException(
                f"Difference in task template owner: {task_owner=} != {username=}"
            )

        print("🔄 Local template differs from hub template, uploading new version...")
        _print_template_differences(sorted_local_template, sorted_hub_template)

        # Create a minimal config for the upload function
        upload_config: dict[str, list[dict[str, Any]]] = {
            "task-templates": [
                {
                    "slug": task_slug,
                    "title": latest_hub_task_template_info.get("title", task_slug),
                    "type": latest_hub_task_template_info.get(
                        "type", "text-classification"
                    ),
                    "description": latest_hub_task_template_info.get("description", ""),
                    "template": local_task_template_path,
                    "tags": latest_hub_task_template_info.get("tags", []),
                }
            ]
        }

        # Upload the new version of the task template
        try:
            update_and_upload_task_templates(
                upload_config,
                task_owner,  # Use the task owner from config
                {},  # No model versions to update
                jwt=jwt,
            )
            print("✅ Successfully uploaded new version of task template")
        except Exception as e:
            print(f"❌ Failed to upload task template: {e}")
            print(f"🔍 Traceback:\n{traceback.format_exc()}")
            raise FailProjectException("Failed to upload task template") from e

        # Get the updated template info to get the new version
        try:
            updated_template_info = get_task_template_info(
                task_owner, task_slug, hub, hub_url
            )
        except Exception as e:
            print(f"❌ Failed to retrieve updated task template info: {e}")
            print(f"🔍 Traceback:\n{traceback.format_exc()}")
            raise FailProjectException(
                "❌ Failed to retrieve updated task template info"
            ) from e
        else:
            template_id = cast(Optional[str], updated_template_info.get("id"))
            if not template_id:
                print(
                    f"❌ Updated task template '{task_owner}/{task_slug}'"
                    f" but new version has no ID"
                )
                raise FailProjectException("Task template ID not found after update")
    else:
        print("✅ Local template matches hub template, no upload needed")

    return template_id


def _find_local_task_template_by_slug(task_slug: str) -> Optional[str]:
    """Finds the local task template YAML file for a given task slug."""
    local_template_path: Optional[str] = None

    for config_path in TASK_TEMPLATES_CONFIG_PATHS:
        try:
            with open(config_path, "r") as f:
                task_templates_config: dict[str, Any] = yaml.safe_load(f)

            # Look for the matching task template by slug
            if "task-templates" in task_templates_config:
                for template_config in task_templates_config["task-templates"]:
                    if template_config.get("slug") == task_slug:
                        local_template_path = template_config.get("template")
                        print(f"📋 Found task template config in: {config_path}")
                        break

            if local_template_path:
                break

        except FileNotFoundError:
            print(f"⚠️  Config file not found: {config_path}")
            continue
        except Exception as e:
            print(f"⚠️  Error parsing config file {config_path}: {e}")
            print(f"🔍 Traceback:\n{traceback.format_exc()}")
            continue

    return local_template_path


def _sort_dict_recursively(obj: Any) -> Any:
    """Recursively sort dictionaries by keys to ensure consistent ordering.

    Args:
        obj: The object to sort (can be dict, list, or any other type).

    Returns:
        The object with all nested dictionaries sorted by keys.
    """
    if isinstance(obj, dict):
        return {
            key: _sort_dict_recursively(value) for key, value in sorted(obj.items())
        }
    elif isinstance(obj, list):
        return [_sort_dict_recursively(item) for item in obj]
    else:
        return obj


def _print_template_differences(
    local_template: dict[str, Any], hub_template: dict[str, Any], prefix: str = ""
) -> None:
    """Print the differences between local and hub templates.

    Args:
        local_template: The local template dictionary.
        hub_template: The hub template dictionary.
        prefix: Prefix for nested keys (used in recursion).
    """
    all_keys = set(local_template.keys()) | set(hub_template.keys())

    for key in sorted(all_keys):
        current_prefix = f"{prefix}.{key}" if prefix else key

        if key not in local_template:
            print(f"  📍 Key missing in local: {current_prefix}")
        elif key not in hub_template:
            print(f"  📍 Key missing in hub: {current_prefix}")
        else:
            local_value = local_template[key]
            hub_value = hub_template[key]

            if isinstance(local_value, dict) and isinstance(hub_value, dict):
                # Recursively compare nested dictionaries
                if local_value != hub_value:
                    _print_template_differences(local_value, hub_value, current_prefix)
            elif local_value != hub_value:
                print(f"  📍 Different value for {current_prefix}:")
                print(f"    Local:  {local_value}")
                print(f"    Hub:    {hub_value}")


def update_project_config(
    target_project_config: ProjectConfig,
    target_task_template_id: str,
    current_project_info: ProjectInfo,
    latest_task_definition: Optional[TaskDefinition],
    hub: BitfountHub,
    hub_url: str,
) -> None:
    """Update a project as needed, considering both task template and variables.

    Args:
        target_project_config: The project configuration as we want to end up using.
        target_task_template_id: The task template ID we want to end up using.
        current_project_info: Project information for its current state.
        latest_task_definition: The latest task definition for that project or None
            if there is no latest task definition.
        hub: The hub connection object.
        hub_url: The hub URL.

    Raises:
        FailProjectException: If the project update fails.

    Returns:
        None if update was successful.
    """
    project_url: str = f"{hub_url}/api/projects/{target_project_config.project_id}"

    # Check if the target task template matches the one currently in use in the task
    # definition.
    needs_template_update: bool
    if latest_task_definition:
        # Compare the current task template ID with the target one
        task_definition_task_template_id = pydash.get(
            latest_task_definition, "taskTemplateSummary.id"
        )
        needs_template_update = (
            task_definition_task_template_id != target_task_template_id
        )
    else:
        # If there is no latest task definition, then we _definitely_ need to
        # update/create
        needs_template_update = True

    # Prepare templated variables update
    desired_variables: dict[str, dict[str, Any]] = _format_template_variables(
        target_project_config.variables
    )

    # Build update payload
    payload: dict[str, Any] = {}

    if needs_template_update:
        payload["taskTemplateId"] = target_task_template_id
        print(f"🔄 Updating task template ID to: {target_task_template_id}")

    payload["templateVariables"] = desired_variables
    print(f"🔄 Updating template variables: {json.dumps(desired_variables, indent=2)}")

    try:
        response = hub.session.patch(url=project_url, json=payload)

        if response.status_code == 200:
            print(f"✅ Successfully updated project {target_project_config.project_id}")
            return
        else:
            print(
                f"❌ Failed to update project {target_project_config.project_id}: {response.status_code}"  # noqa: E501
            )
            print(f"Response: {response.text}")
            raise FailProjectException(
                f"Failed to update project: {target_project_config.project_id}:"
                f" {response.status_code}"
            )
    except Exception as e:
        print(f"❌ Error updating project {target_project_config.project_id}: {e}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        if isinstance(e, FailProjectException):
            # If the exception is a FailProjectException, re-raise it as-is to avoid
            # losing the original context
            raise
        else:
            raise FailProjectException(
                f"Failed to update project: {target_project_config.project_id}: {e}"
            ) from e


def _format_template_variables(variables: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Format variables into the expected template variables format.

    Args:
        variables: Dictionary of variable names to values.

    Returns:
        Formatted template variables dictionary.
    """
    formatted = {}
    for var_name, var_value in variables.items():
        formatted[var_name] = {"value": var_value, "mode": TASK_VARIABLE_MODE}
    return formatted


def process_project(
    project_config: ProjectConfig,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> ProcessResult:
    """Process a single project configuration.

    Args:
        project_config: The project configuration to process.
        username: The authenticated username.
        jwt: The JWT token.
        hub: The hub connection object.
        hub_url: The hub URL.

    Returns:
        ProcessResult enum value.
    """
    print(f"\n🔄 Processing project: {project_config.project_id}")
    print(f"   Task template: {project_config.task_owner}/{project_config.task_slug}")
    print(f"   Variables: {project_config.variables}")

    # Get current project info
    current_project: ProjectInfo
    try:
        current_project = get_project_info(project_config.project_id, hub, hub_url)
        if current_project.get("status") != "PUBLISHED":
            print(
                f"⚠️ Skipping project {project_config.project_id} because it is not published"  # noqa: E501
            )
            return ProcessResult.SKIPPED
    except FailProjectException:
        print(f"❌ Failed to get project info for {project_config.project_id}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        return ProcessResult.FAILED

    # Get the task template ID needed for the project
    try:
        if isinstance(project_config.task_template_version, int):
            print(
                f"❌ Specific task template version is not yet supported:"
                f" got {project_config.task_template_version=}"
            )
            return ProcessResult.FAILED
        elif project_config.task_template_version == "latest":
            # Check and update task template if needed, getting the latest task
            # template ID
            _update_project_latest(
                project_config,
                current_project,
                username,
                jwt,
                hub,
                hub_url,
            )
        elif project_config.task_template_version == "project-current":
            # Get the current task template ID from the project (if it exists) and
            # use that, rather than updating
            _update_project_project_current(
                project_config,
                current_project,
                username,
                jwt,
                hub,
                hub_url,
            )
        elif project_config.task_template_version == "sdk-skip":
            # Compare task template version, skip if different, update template
            # variables if same
            _update_project_sdk_skip(
                project_config,
                current_project,
                username,
                jwt,
                hub,
                hub_url,
            )
        elif project_config.task_template_version == "sdk-fail":
            # Compare task template version, fail if different, update template
            # variables if same
            _update_project_sdk_fail(
                project_config,
                current_project,
                username,
                jwt,
                hub,
                hub_url,
            )
        else:
            print(  # type: ignore[unreachable] # Reason: This is the fallback case
                f"❌ Got unexpected task-template-version option:"
                f" got {project_config.task_template_version=}"
            )
            return ProcessResult.FAILED
    except SkipProjectException:
        return ProcessResult.SKIPPED
    except FailProjectException:
        return ProcessResult.FAILED
    else:
        return ProcessResult.SUCCESS


def _update_project_latest(
    project_config: ProjectConfig,
    current_project_info: ProjectInfo,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> None:
    """For a given project, update config task template to the latest version.

    Will also update any template variables if needed.
    """
    # Get the latest task template ID
    latest_task_template_id = get_or_update_latest_task_template(
        project_config, username, jwt, hub, hub_url
    )

    latest_task_definition = get_latest_task_definition_for_project(
        project_config.project_id, hub, hub_url
    )

    update_project_config(
        project_config,
        latest_task_template_id,
        current_project_info,
        latest_task_definition,
        hub,
        hub_url,
    )


def _update_project_project_current(
    project_config: ProjectConfig,
    current_project_info: ProjectInfo,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> None:
    """Update only the project config template variables, not the task template itself.

    The only time the task template for the project is set/updated is if there is no
    task template yet at all.
    """  # noqa: E501
    latest_task_def = get_latest_task_definition_for_project(
        project_config.project_id, hub, hub_url
    )

    # If there is no (latest) task definition then we fallback to creating as though
    # the project task version was "latest", creating its first task definition.
    if not latest_task_def:
        print(
            f"⚠️ Could not find latest task definition"
            f" for project {project_config.project_id}."
            f" Will create new task definition."
        )
        return _update_project_latest(
            project_config, current_project_info, username, jwt, hub, hub_url
        )

    # Extract the template ID from the latest task definition. If it doesn't exist,
    # we don't want to update as it may be a hardcoded task definition rather than
    # one backed by task templates.
    template_id: Optional[str] = pydash.get(latest_task_def, "taskTemplateSummary.id")
    if not template_id:
        print(
            f"❌ Latest task definition for project {project_config.project_id} exists"
            f" but contained no task template ID."
            f" It may be a hardcoded definition."
            " Not overwriting."
        )
        raise FailProjectException(
            "Failed to get task template ID from latest task definition"
        )

    update_project_config(
        project_config, template_id, current_project_info, latest_task_def, hub, hub_url
    )


def _update_project_sdk_skip(
    project_config: ProjectConfig,
    current_project_info: ProjectInfo,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> None:
    """If project’s task template is not the same as the SDK version then skip updating the project.

    Will log out details about the difference though.
    """  # noqa: E501
    return _update_project_sdk_common(
        project_config,
        current_project_info,
        username,
        jwt,
        hub,
        hub_url,
        skip_or_fail="SKIP",
    )


def _update_project_sdk_fail(
    project_config: ProjectConfig,
    current_project_info: ProjectInfo,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
) -> None:
    """If project’s task template is not the same as the SDK version then produce failure."""  # noqa: E501
    return _update_project_sdk_common(
        project_config,
        current_project_info,
        username,
        jwt,
        hub,
        hub_url,
        skip_or_fail="FAIL",
    )


def _update_project_sdk_common(
    project_config: ProjectConfig,
    current_project_info: ProjectInfo,
    username: str,
    jwt: ExternallyManagedJWT,
    hub: BitfountHub,
    hub_url: str,
    skip_or_fail: Literal["SKIP", "FAIL"],
) -> None:
    """Common logic for sdk-skip and sdk-fail options."""
    # Get the latest task template ID
    latest_task_template_id = get_or_update_latest_task_template(
        project_config, username, jwt, hub, hub_url
    )

    latest_task_definition = get_latest_task_definition_for_project(
        project_config.project_id, hub, hub_url
    )

    # If there is no (latest) task definition then we simply skip
    if not latest_task_definition:
        print(
            f"⚠️ Could not find latest task definition"
            f" for project {project_config.project_id}."
            f" Skipping."
        )
        raise SkipProjectException("No task definition for project")

    # Extract the template ID from the latest task definition. If it doesn't exist,
    # we don't want to update as it may be a hardcoded task definition rather than
    # one backed by task templates.
    current_task_template_id: Optional[str] = pydash.get(
        latest_task_definition, "taskTemplateSummary.id"
    )
    if not current_task_template_id:
        print(
            f"❌ Latest task definition for project {project_config.project_id} exists"
            f" but contained no task template ID."
            f" It may be a hardcoded definition."
            " Unable to handle."
        )
        raise FailProjectException(
            "Failed to get task template ID from latest task definition"
        )

    if current_task_template_id != latest_task_template_id:
        issue_symbol = "⚠️" if skip_or_fail == "SKIP" else "❌"
        issue_msg = (
            f"{issue_symbol} Project {project_config.project_id} task template is"
            f" not the same as the latest version."
            f" Current task template ID: {current_task_template_id},"
            f" SDK task template ID: {latest_task_template_id}."
        )
        if skip_or_fail == "SKIP":
            issue_msg += " Skipping."
        print(issue_msg)

        if skip_or_fail == "SKIP":
            raise SkipProjectException(
                "Project's task template is not the same as SDK version"
            )
        else:
            raise FailProjectException(
                "Project's task template is not the same as SDK version"
            )
    else:
        # If they are the same, then do an update (which will update the variables if
        # needed)
        update_project_config(
            project_config,
            current_task_template_id,
            current_project_info,
            latest_task_definition,
            hub,
            hub_url,
        )


def main(
    config_file: str,
    username: str,
    password: str,
) -> None:
    """Main function to update projects from configuration file.

    Args:
        config_file: Path to the YAML configuration file.
        username: The username for authentication.
        password: The password for authentication.
    """
    if not config_file or not username or not password:
        print("❌ config_file, username, and password are all required!")
        sys.exit(1)

    # Load configuration
    try:
        projects: list[ProjectConfig] = load_config(config_file)
        if not projects:
            print("❌ No projects found in configuration file!")
            sys.exit(1)
        print(f"📋 Loaded {len(projects)} projects from configuration")
    except Exception as e:
        print(f"❌ Failed to load configuration file: {e}")
        print(f"🔍 Traceback:\n{traceback.format_exc()}")
        sys.exit(1)

    # Get JWT for authentication
    try:
        print(f"🔐 Authenticating as: {username}")
        access_token: str
        expires_in: int
        access_token, expires_in = _get_user_token(username, password)
        jwt: ExternallyManagedJWT = ExternallyManagedJWT(
            jwt=access_token,
            expires=datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            # Refreshing not necessary as this is not a long-running script
            get_token=lambda: None,  # type: ignore[arg-type, return-value]
        )
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)

    # Create hub connection
    hub_url = get_hub_url()
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)

    # Process each project
    success_count: int = 0
    failure_count: int = 0
    skipped_count: int = 0
    ownership_skipped_count: int = 0

    for project_config in projects:
        try:
            # Check if the authenticated user owns the project
            if username != project_config.project_owner:
                print(
                    f"\n⚠️  Skipping project {project_config.project_id} because authenticated user '{username}' "  # noqa: E501
                    f"does not own this project (owned by '{project_config.project_owner}')"  # noqa: E501
                )  # noqa: E501
                ownership_skipped_count += 1
                continue

            result: ProcessResult = process_project(
                project_config, username, jwt, hub, hub_url
            )
            if result == ProcessResult.SUCCESS:
                success_count += 1
            elif result == ProcessResult.SKIPPED:
                skipped_count += 1
            else:  # ProcessResult.FAILED
                failure_count += 1
        except Exception as e:
            print(
                f"❌ Unexpected error processing project {project_config.project_id}: {e}"  # noqa: E501
            )
            failure_count += 1

    # Summary
    print("\n📊 Summary:")
    print(f"   ✅ Successfully processed: {success_count}")
    print(f"   ⚠️ Skipped (ownership): {ownership_skipped_count}")
    print(f"   ⚠️ Skipped (other): {skipped_count}")
    print(f"   ❌ Failed: {failure_count}")

    if failure_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    Fire(main)
