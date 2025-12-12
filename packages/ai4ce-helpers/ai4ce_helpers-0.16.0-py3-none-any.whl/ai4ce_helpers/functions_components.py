import ast
import json
from pathlib import Path
from typing import List

import pandas as pd
import toml

from ._backend_calls import _backend_GET
from ._backend_calls import _backend_POST
from ._backend_calls import _backend_PUT
from .functions_projects import get_sys_arch
from .logging_setup import logger_ai4cehelper


def get_tags_from_string(str_of_tags: str) -> list[str]:
    """
    example_tags_str = "['satellite', 'power', 'solar-panels']"
    check https://gitlab.com/ai4ce/ai4ce-03-backend/-/blob/main/backend/v2/schemas/components/_uid_maps.py for valid tags
    """
    # The string representation of a list of tags

    # Convert the string to an actual list using ast.literal_eval
    tags: list = ast.literal_eval(str_of_tags)
    return tags


def comp_create(comp_info: dict) -> dict:
    """Create a new component in the backend.
    Params:
        comp_info(dict): Information about the component
    Returns:
        dict:
    """
    status_code, msg = _backend_POST(endpoint=f"/v2/components/", data=comp_info)
    return status_code, msg


def export_components() -> dict:
    """Fetches all decisions from the DecisionDB and returns them as a dictionary.

    Returns:
        dict: A dictionary containing all decisions fetched from the DecisionDB.
    """
    status_code, response = _backend_GET(endpoint="/v2/components/export/")
    return response


def get_comp_statistics() -> dict:

    status_code, response = _backend_GET(endpoint="/v2/streamlit/db/stats/components")
    return response


def get_comp_statistics_all_systems() -> dict:
    """
    Retrieves component statistics for all systems.

    Returns:
        dict: Statistics data for all systems, as retrieved from the backend.
    """

    status_code, response = _backend_GET(endpoint="/v2/streamlit/db/stats")
    return response


def split_uid(uid: str) -> tuple[str, str, str, int | str]:
    """Splits a component UID into its constituent parts: type, subtype, and name.

    Args:
        uid (str): The UID of the component in the format 'type-subtype-name'.

    Returns:
        tuple: A tuple containing the type, subtype, and name of the component.
    """
    try:
        system_uid, subsystem_uid, component_class, component_id = uid.split("_", 3)
        try:
            component_id = int(component_id)
        except ValueError:
            pass
        return system_uid, subsystem_uid, component_class, component_id
    except ValueError:
        raise ValueError(
            "Invalid UID format. Expected UID format: <system>_<subsystem>_<component_class>_<component_id>"
        )


def get_all_enabled_comps_from_system(project_id: int) -> list:
    """Collect the enabled components from a project's system architecture.

    Retrieves the system definition for ``project_id`` with ``get_sys_arch``
    and walks each subsystem, skipping their ``requirements`` entries. For
    component dictionaries marked with ``"enabled": True`` the component key is
    added to the result list. When a component value is a list, any dictionary
    items in the list with ``"enabled": True`` are appended as-is.

    Parameters:
        project_id (int): Identifier of the project whose system components
            should be inspected.

    Returns:
        list: Enabled component identifiers (strings) and/or component payload
        dictionaries depending on how they are represented in the system
        definition.
    """

    enabled_components: list[str] = []
    # Components listed here will be excluded from get_all_enabled_comps_from_system.
    # Populate manually with subsystem and/or component identifiers (e.g. "eps",
    # "com.opticals"). Matching applies to both the dotted path and individual
    # segments.
    # COMPONENT_BLACKLIST: List[str] = ["AODCS", "CDH", "COM", "EPS", "PAYLOAD", "STRUCTURE", "TCS"]

    try:
        system: dict = get_sys_arch(project_id)
    except KeyError:
        logger_ai4cehelper.error(f"(gaecfs) No system architecture found for project {project_id}.")
        return enabled_components

    for subsystem_key, subsystem_value in system.items():
        if isinstance(subsystem_value, dict) and subsystem_key not in ["requirements"]:
            for component_key, component_value in subsystem_value.items():
                if isinstance(component_value, dict) and component_key not in ["requirements"]:
                    if component_value.get("enabled") is True:
                        enabled_components.append(component_key)
                elif isinstance(component_value, list):
                    for item in component_value:
                        if isinstance(item, dict):
                            if item.get("enabled") is True:
                                enabled_components.append(item)
    return enabled_components
