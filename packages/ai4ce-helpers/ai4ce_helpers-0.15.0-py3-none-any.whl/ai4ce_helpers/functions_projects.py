from pathlib import Path
import warnings
import datetime
import pandas as pd
import httpx
from datetime import timezone
from typing import Literal
from ._backend_calls import _backend_GET
from ._backend_calls import _backend_POST
from ._backend_calls import _backend_PUT
from .functions import load_file, get_toml_from_url
from .logging_setup import logger_ai4cehelper
from deprecated import deprecated


def get_universal_sysarch_comp_mapping() -> dict:
    """
    Retrieves a universal mapping of system architecture and component structure for CubeSat systems.

    This function downloads the CubeSat system architecture mapping from a remote TOML file hosted on GitLab.
    It extracts all subsystem entries for CubeSat that are represented as uppercase keys (by convention, subsystem keys are all uppercase),
    and returns them in a hierarchical dictionary format suitable for universal lookups or further processing.

    Returns:
        dict: A dictionary containing the CubeSat system mapping, where each subsystem (uppercase key) maps to its respective components.

    Example:
        {
            "cubesat": {
                "ADCS": {...},
                "CDHS": {...},
                ...
            }
        }
    """
    url = "https://gitlab.com/ai4ce/AI4CE/-/raw/main/ai4ce/system_tags.toml?ref_type=heads"
    system_tags: dict = get_toml_from_url(url=url)

    response: dict = {}
    response["cubesat"] = {}

    for key, value in system_tags["CubeSat"].items():
        if key.isupper():  # subsystems are all uppercase
            response["cubesat"][key] = value
    return response

def create_new_project(project_info: dict):
    """Create a new project in the backend.
    Params:
        project_info(dict):
    Returns:
        dict: Backend version of the project.
    Raises:
        Exception: If there is an error creating the new project.
    """
    status_code, project = _backend_POST(endpoint=f"/v2/projects/", data=project_info)
    if status_code != 201:
        logger_ai4cehelper.error(f"(cnp) Error creating new project ({status_code}): {project}")
        raise Exception(f"Error creating new project ({status_code}): {project}")
    return project


def get_list_of_all_project_infos() -> list[tuple[int, str, str]]:
    # check for refactoring
    """A function to connect to the backend and get a list of all projects
    in the current project data base.

    Returns:
        tuple[int, str, str]: A list of tuples containing project ID, project name, and last modified date.
    
    Raises:
        Exception: If there is an error fetching the list of projects.
    """

    status_code, projects = _backend_GET(endpoint=f"/v2/projects/")
    project_ids: list[tuple[int, str, str]] = []
    if status_code == 200:
        for project in projects:
            project_ids.append((project["id"], project["project_name"], project["modified"]))
        return project_ids
    else:
        logger_ai4cehelper.error(f"(gloapi) Error fetching projects ({status_code}): {projects}")
        raise Exception(f"Error fetching projects ({status_code}): {projects}")


def get_project_info(project_id: int) -> dict:
    status_code, project_info = _backend_GET(endpoint=f"/v2/projects/{project_id}/")
    if status_code != 200:
        logger_ai4cehelper.error(f"(gpi) Error fetching project info ({status_code}): {project_info}")
        raise Exception(f"Error fetching project info ({status_code}): {project_info}")
    return project_info


def set_project_name(project_id: int, project_name: str) -> dict:
    """A function to set the project name of a specific project, identified by its ID.

    Params:
        project_id   (int): The project ID
        project_name (str): Name of the project/mission, eg OPS-Sat
    Returns:
        dict: Backend version of the general project info.
    Raises:
        KeyError: If the project is not found.
        Exception: If there is an error setting the project name.
    """

    data = {
        "id": project_id,
        "project_name": project_name,
    }

    # status, msg = _backend_put(endpoint=f"/v2/projects/{project_id}", data=data)
    # return (status, msg)
    status_code, response = _backend_PUT(endpoint=f"/v2/projects/{project_id}/", data=data)
    if status_code == 404:
        logger_ai4cehelper.error(f"(spn) Project with ID {project_id} not found.")
        raise KeyError(f"Project with ID {project_id} not found.")
    if status_code != 200:
        logger_ai4cehelper.error(f"(spn) Error setting project name ({status_code}): {response}")
        raise Exception(f"Error setting project name ({status_code}): {response}")
    return response


def get_recent_project() -> tuple[int, str, str]:
    """A function to get the most recently modified project from the backend.
    Returns:
        tuple[int, str, str]: A tuple containing project ID, project name, and last modified date.
    Raises:
        Exception: If there is an error fetching the recent project.
    """
    status_code, response = _backend_GET(endpoint=f"/v2/projects/recent/")
    if status_code != 200:
        logger_ai4cehelper.error(f"(grp) Error fetching recent project ({status_code}): {response}")
        raise Exception(f"Error fetching recent project ({status_code}): {response}")
    return (response["id"], response["project_name"], response["modified"])


def get_mission_orbit(project_id: int) -> dict:
    """A function to get the mission orbit info for a specific project based on its ID.
    Params:
        project_id (int): The project ID

    Returns:
        dict: Keplerian elements to define the orbit

    Raises:
        KeyError: If no mission is found for the given project ID.
        KeyError: If no orbit information is found in the mission data.
        Exception: If there is another error fetching the mission orbit.
    """

    status_code, response = _backend_GET(endpoint=f"/v2/projects/{project_id}/mission/")
    if status_code == 404:
        logger_ai4cehelper.error(f"(gmo) No mission orbit found for project {project_id}.")
        raise KeyError(f"No mission orbit found for project {project_id}.")
    if status_code != 200:
        logger_ai4cehelper.error(f"(gmo) Error fetching mission orbit ({status_code}): {response}")
        raise Exception(f"Error fetching mission orbit ({status_code}): {response}")
    if "orbit" not in response:
        logger_ai4cehelper.error(f"(gmo) No orbit information found in mission data")
        raise KeyError("No orbit information found in mission data")
    return response["orbit"]


def set_mission_orbit(project_id: int, orbit_info: dict) -> dict:
    """A function to set the orbit in the project database. Will create an empty mission parent if it does not exist.
    Params:
        project_id (int): The project ID
        orbit_info(dict): Information about the satellite's orbit

    Returns:
        dict: Backend version of the mission orbit or the status_code and error message.

    Raises:
        Exception: If there is an error creating or updating the mission orbit.
    """
    # check if project exists
    status_code, project_info = _backend_GET(endpoint=f"/v2/projects/{project_id}/")
    if status_code != 200:
        logger_ai4cehelper.error(f"(smo) Error fetching project info ({status_code}): {project_info}")
        raise Exception(f"Error fetching project info ({status_code}): {project_info}")

    status_code, mission_info = _backend_GET(endpoint=f"/v2/projects/{project_id}/mission/")
    if status_code == 404:
        logger_ai4cehelper.info(f"(smo) No mission info found for project {project_id}. Creating new mission info.")
        mission_info = {
            "mission_name": f"Mission {project_info['project_name']}",
            "orbit": orbit_info,
        }
        status_code, response = _backend_POST(endpoint=f"/v2/projects/{project_id}/mission/", data=mission_info)
        if status_code != 201:
            logger_ai4cehelper.error(f"(smo) Error creating mission info ({status_code}): {response}")
            raise Exception(f"Error creating mission info ({status_code}): {response}")
        return response
    elif status_code == 200:
        # update possible mission_info["orbit"] with new orbit_info
        logger_ai4cehelper.info(f"(smo) Mission info found for project {project_id}. Updating orbit info.")
        if "orbit" not in mission_info:
            mission_info["orbit"] = {}
        mission_info["orbit"].update(orbit_info)
        status_code, response = _backend_PUT(endpoint=f"/v2/projects/{project_id}/mission/", data=mission_info)
        if status_code != 200:
            logger_ai4cehelper.error(f"(smo) Error updating mission info ({status_code}): {response}")
            raise Exception(f"Error updating mission info ({status_code}): {response}")
        return response
    else:
        logger_ai4cehelper.error(f"(smo) Error fetching mission info ({status_code}): {mission_info}")
        raise Exception(f"Error fetching mission info ({status_code}): {mission_info}")


def get_enabled_components(nested_dict, enabled_components=None) -> list:
    # check for refactoring
    """
    Recursively traverses a nested dictionary to find and return a list of components that are enabled.

    Parameters:
        nested_dict (dict): The nested dictionary to traverse.
        enabled_components (list, optional): A list to store the names of the enabled components.
                                         Defaults to None, in which case a new list is created.

    Returns:
        list: A list of the names of the enabled components.
    """

    if enabled_components is None:
        enabled_components = []

    for key, value in nested_dict.items():
        if isinstance(value, dict):
            if (value.get("enabled") == True or value.get("Enabled") == True):
                enabled_components.append(key)
            get_enabled_components(value, enabled_components)

    return enabled_components


def traverse_and_modify(d: dict, sys_config_enabled: dict):
    # check for refactoring
    for key, value in d.items():
        if isinstance(value, dict):
            component = key
            traverse_and_modify(d=value, sys_config_enabled=sys_config_enabled)
        else:
            # This block executes only if `value` is not a dict, i.e., at the deepest level
            # if d["Enabled"] is True or d["Enable"] is True or :
            try:
                if d["Enabled"] is True:
                    sys_config_enabled.update(
                        enable_component(
                            component_name=key,
                            data=load_file(Path("data/backend_sys_default.json")),
                        )
                    )
            except KeyError as e:  # what are you doing here -.-
                print("Error: ", e)


def enable_component(component_name: str, data: dict) -> dict:
    # check for refactoring
    """Recursively search for a component in the nested dictionary from the backend
    and set 'enabled' to True if the feature name matches any key or value (case-insensitive).

    Parameters:
        data (dict): The nested dictionary to search within.
        feature_name (str): The feature name to search for, case-insensitively.

    Returns:
        dict: edited dict
    """

    for key, value in data.items():
        #  print(key, value)
        if isinstance(value, dict):
            enable_component(component_name, value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    enable_component(component_name, item)
        if key.lower() == component_name.lower() or str(value).lower() == component_name.lower():
            data["enabled"] = True
    return data


def set_sys_arch(project_id: int, sys_arch: dict) -> dict:
    """A function to set the system architecture in the project database. Updates the existing architecture if it exists.
    Params:
        project_id (int): The project ID
        sys_arch (dict): Information about the satellite's modules, which form the system architecture
    Returns:
        dict: Backend version of the system architecture.
    Raises:
        Exception: If there is an error creating or updating the system architecture.
    """

    status_code, system = _backend_GET(endpoint=f"/v2/projects/{project_id}/system/")
    if status_code == 404:
        logger_ai4cehelper.info(
            f"(ssa) No system architecture found for project {project_id}. Creating new system architecture."
        )
        status_code, response = _backend_POST(endpoint=f"/v2/projects/{project_id}/system/", data=sys_arch)
        if status_code != 201:
            logger_ai4cehelper.error(f"(ssa) Error creating system architecture ({status_code}): {response}")
            raise Exception(f"Error creating system architecture ({status_code}): {response}")
        return response
    elif status_code == 200:
        logger_ai4cehelper.info(
            f"(ssa) System architecture found for project {project_id}. Updating system architecture."
        )
        system.update(sys_arch)
        status_code, response = _backend_PUT(endpoint=f"/v2/projects/{project_id}/system/", data=system)
        if status_code != 200:
            logger_ai4cehelper.error(f"(ssa) Error updating system architecture ({status_code}): {response}")
            raise Exception(f"Error updating system architecture ({status_code}): {response}")
        return response


def get_sys_arch(project_id: int) -> dict:
    """A function to get the system configuration info for a specific project based on its ID.
    Params:
        project_id (int): The project ID

    Returns:
        dict: Backend version of the system architecture.

    Raises:
        KeyError: If no system architecture is found for the given project ID.
        Exception: If there is another error fetching the system architecture.
    """

    status_code, response = _backend_GET(endpoint=f"/v2/projects/{project_id}/system/")
    if status_code == 404:
        logger_ai4cehelper.error(f"(gsa) No system architecture found for project {project_id}.")
        raise KeyError(f"No system architecture found for project {project_id}.")
    if status_code != 200:
        logger_ai4cehelper.error(f"(gsa) Error fetching system architecture ({status_code}): {response}")
        raise Exception(f"Error fetching system architecture ({status_code}): {response}")
    return response


#  set_comp_list(project: int, not_yet_defined: dict)
# For each selected system generator, we need a place to store the corresponding found comp lists
# Every generator can produce n sets of components
@deprecated(reason="update_sys_generator() is deprecated, use set_sys_generator() instead.", version="0.10.12")
def update_sys_generator(project_id: int, sys_gen_info: dict) -> dict:
    """Deprecated: update_sys_generator is deprecated, use set_sys_generator instead."""
    warnings.warn("update_sys_generator is deprecated, use set_sys_generator instead.", DeprecationWarning)
    return set_sys_generator(project_id=project_id, sys_gen_info=sys_gen_info)


def set_sys_generator(project_id: int, sys_gen_info: dict) -> dict:
    """A function to set the system generator info in the project database. Updates the existing generator if it exists.
    Params:
        project_id (int): The project ID 
        sys_gen_info (dict): Information about the system generator
    Returns:
        dict: Backend version of the system generator.
    Raises:
        Exception: If there is an error creating or updating the system generator info.
    """
    if "id" in sys_gen_info:
        status_code, existing_sys_gen = _backend_GET(endpoint=f"/v2/projects/{project_id}/sysgen/{sys_gen_info['id']}/")
        if status_code == 200:
            logger_ai4cehelper.info(
                f"(ssg) System generator info found for project {project_id}. Updating system generator info."
            )
            existing_sys_gen.update(sys_gen_info)
            status_code, response = _backend_PUT(
                endpoint=f"/v2/projects/{project_id}/sysgen/{sys_gen_info['id']}/",
                data=existing_sys_gen,
            )
            if status_code != 200:
                logger_ai4cehelper.error(f"(ssg) Error updating system generator info ({status_code}): {response}")
                raise Exception(f"Error updating system generator info ({status_code}): {response}")
            return response
    logger_ai4cehelper.info(f"(ssg) Creating new system generator info for project {project_id}.")
    status_code, response = _backend_POST(endpoint=f"/v2/projects/{project_id}/sysgen/", data=sys_gen_info)
    if status_code != 201:
        logger_ai4cehelper.error(f"(ssg) Error creating system generator info ({status_code}): {response}")
        raise Exception(f"Error creating system generator info ({status_code}): {response}")
    return response


def set_trained_model(
    project_id: int,
    sysgen_id: int,
    environment_settings: dict = {},
    model_file: bytes = None,
) -> dict:

    if not model_file and not environment_settings:
        logger_ai4cehelper.error(f"(stm) Either environment_settings or model_file must be provided.")
        raise ValueError("Either environment_settings or model_file must be provided.")

    sys_gen = {
        "environment_settings": environment_settings,
        "id": sysgen_id,
    }

    sysgen_db = update_sys_generator(project_id=project_id, sys_gen_info=sys_gen)

    if model_file:
        status_code, response = _backend_GET(endpoint=f"/v2/projects/{project_id}/sysgen/{sysgen_id}/model/")
        if status_code == 404:
            logger_ai4cehelper.info(
                f"(stm) No trained model found for sysgen {sysgen_id} in project {project_id}. Creating new trained model."
            )
            status_code, response = _backend_POST(
                endpoint=f"/v2/projects/{project_id}/sysgen/{sysgen_id}/model/",
                data={"model_file": model_file},
            )
            if status_code != 201:
                logger_ai4cehelper.error(f"(stm) Error creating trained model ({status_code}): {response}")
                raise Exception(f"Error creating trained model ({status_code}): {response}")
            return response
        elif status_code == 200:
            logger_ai4cehelper.info(
                f"(stm) Trained model found for sysgen {sysgen_id} in project {project_id}. Updating trained model."
            )
            status_code, response = _backend_PUT(
                endpoint=f"/v2/projects/{project_id}/sysgen/{sysgen_id}/model/",
                data={"model_file": model_file},
            )
            if status_code != 200:
                logger_ai4cehelper.error(f"(stm) Error updating trained model ({status_code}): {response}")
                raise Exception(f"Error updating trained model ({status_code}): {response}")
            return response
        raise Exception(f"(stm) Unexpected status code ({status_code}): {response}")
    return sysgen_db


def get_prepared_system_generator_info(project_id: int) -> list:
    """A function to get all prepared system generators.
    Params:
        project_id (int): The project ID

    Returns:
        list: list of dictionaries with infos for the prepared system generators
    """

    status_code, response = _backend_GET(endpoint=f"/v2/projects/{project_id}/sysgen/")
    if status_code != 200:
        logger_ai4cehelper.error(f"(gpsg) Error fetching prepared system generators ({status_code}): {response}")
        raise Exception(f"Error fetching prepared system generators ({status_code}): {response}")
    return response


def set_sys_arch_defaults(system: dict, project_id: int) -> dict:
    """Translate a system configuration from a TOML file dictionary previously handled by load_file() to a format that can be uploaded to the backend.

    Parameters:
    system (dict): The system configuration in TOML format.

    Returns:
    dict: The system configuration in a format that can be uploaded to the backend.
    """

    sys_arch_example = {
        "system_type": "string",
        "satellite_class": "string",
        "OAP_W": 0,
        "requirements": {},
        "aodcs": {
            "enabled": False,
            "amount_of_entities": 0,
            "description": "string",
            "eFunctions": [],
            "type": "string",
            "components": [],
            "depending_parameters": [],
            "cmg": {
                "enabled": False,
                "amount_of_entities": 0,
                "description": "string",
                "eFunctions": [],
                "requirements": {},
            },
            "magnetorquers": {
                "enabled": False,
                "amount_of_entities": 0,
                "description": "string",
                "eFunctions": [],
                "requirements": {},
            },
        },
        "tcs": {
            "enabled": False,
            "amount_of_entities": 0,
            "description": "string",
            "eFunctions": [],
            "requirements": {},
            "coatings": {
                "enabled": False,
                "amount_of_entities": 0,
                "description": "string",
                "eFunctions": [],
                "requirements": {},
            },
            "heaters": {
                "enabled": False,
                "amount_of_entities": 0,
                "description": "string",
                "eFunctions": [],
                "requirements": {},
            },
        },
    }

    sys_config_enabled = {}
    # Loading System Configuration
    for key, value in system.items():
        if isinstance(value, dict):
            traverse_and_modify(d=value, sys_config_enabled=sys_config_enabled)

    response = set_sys_arch(project_id=project_id, sys_arch=sys_config_enabled)
    pass
    return response


def set_new_project(project_info: dict) -> tuple[int, dict]:
    """Create a new project in the backend. Updates the project if it already exists.
    Params:
        project_info(dict): Information about the project to create or update.
    Returns:
        tuple[int, dict]: Status code and backend version of the project.
    Raises:
        Exception: If there is an error creating the new project.
    """
    if "id" in project_info:
        status_code, existing_project = _backend_GET(endpoint=f"/v2/projects/{project_info['id']}/")
        if status_code == 200:
            logger_ai4cehelper.info(
                f"(snp) Project with ID {project_info['id']} found. Updating existing project."
            )
            existing_project.update(project_info)
            status_code, response = _backend_PUT(
                endpoint=f"/v2/projects/{project_info['id']}/",
                data=existing_project,
            )
            if status_code != 200:
                logger_ai4cehelper.error(f"(snp) Error updating project ({status_code}): {response}")
                raise Exception(f"Error updating project ({status_code}): {response}")
            return status_code, response
    logger_ai4cehelper.info(f"(snp) Creating new project.")
    status_code, response = _backend_POST(endpoint=f"/v2/projects/", data=project_info)
    if status_code != 201:
        logger_ai4cehelper.error(f"(snp) Error creating new project ({status_code}): {response}")
        raise Exception(f"Error creating new project ({status_code}): {response}")
    return status_code, response

def set_sysgen_time(project_id: int, sysgen_id:int, mode: Literal["start", "end", "last_update"]) -> dict:
    """A function to set the start time of a system generator in the project database.
    Params:
        project_id (int): The project ID
        sysgen_id (int): The system generator ID
        mode (Literal["start", "end", "last_update"]): The time mode to set.
    Returns:
        dict: Backend version of the system generator.
    Raises:
        Exception: If there is an error updating the system generator info.
    """
    status_code, sysgen_info_db = _backend_GET(endpoint=f"/v2/projects/{project_id}/sysgen/{sysgen_id}/")
    if status_code != 200:
        logger_ai4cehelper.error(f"(sst) Error fetching system generator info ({status_code}): {sysgen_info_db}")
        raise Exception(f"Error fetching system generator info ({status_code}): {sysgen_info_db}")

    sysgen_info =  {}
    sysgen_info[f"time_{mode}"] = datetime.datetime.now(timezone.utc).isoformat()

    status_code, response = _backend_PUT(
        endpoint=f"/v2/projects/{project_id}/sysgen/{sysgen_id}/",
        data=sysgen_info,
    )
    if status_code != 200:
        logger_ai4cehelper.error(f"(sst) Error updating system generator info ({status_code}): {response}")
        raise Exception(f"Error updating system generator info ({status_code}): {response}")
    return response


# def get_trained_model(project_id: int) -> mode: ASKYOUNES
#     pass


# def set_train_log(project_id: int, logs: ASKYOUNES) -> DB_response: ASKALEX
#     pass


# def get_train_logs(project_id: int) -> logs: ASKYOUNE   pass

def generate_mermaid_code(enabled_systems: list, rewards: dict = None, system_class: str = 'cubesat') -> str:
    """Generate mermaid code for a system architecture diagram based on enabled systems and optional rewards.

    Parameters:
        enabled_systems (list): A list of enabled system component names. 
        rewards (dict, optional): A dictionary mapping component names to their reward values.
        example_enabled_systems = ["eps", "batteries"]
    Returns:
        str: The generated mermaid code as a string.
    """
    mcode = []
    if system_class == 'cubesat':
        hierarchy = get_universal_sysarch_comp_mapping()
    subsystems = list(hierarchy[system_class].keys())
    subsystems_lower = [subsystem.lower() for subsystem in subsystems]
    components = [item for sublist in hierarchy[system_class].values() for item in sublist]
    # key_map = {
    #     "batteries": "r_bat",
    #     "solar_panels": "r_sp",
    #     "frames": "r_frame",
    #     "obc": "r_OBC",
    #     "cameras": "r_cam",
    #     "transceivers": "r_TRX",
    #     "reaction_wheels": "r_rw",
    #     "AODCS": "r_AODCS",
    #     "EPS": "r_EPS",
    #     "CDH": "r_CDH",
    #     "STRUCTURE": "r_Structure",
    #     "COM": "r_COMS",
    #     "PAYLOAD": "r_PL"
    # }
    mcode = ["graph TB"]
    mcode.append(
        "    classDef pink fill:#ff00ff,stroke:#000,stroke-width:2px;"
        " classDef blue color:#FFFFFF,fill:#055471,stroke:#000,stroke-width:2px;"
        " classDef yellow fill:#FFC443,stroke:#000,stroke-width:2px,color:#000;"
    )
    mcode.append(f"   {system_class}")
    mcode.append(f"    class {system_class} yellow;")
    mcode.append("    subgraph Subsystems")
    for subsystem in subsystems_lower:
        if subsystem in enabled_systems:
            mcode.append(f"    {subsystem.upper()} ")
            mcode.append(f"    class {subsystem.upper()} pink;")
    mcode.append("    end")
    mcode.append(f"    class Subsystems blue;")
    mcode.append("    subgraph Components")
    for component in components:
        if component in enabled_systems:
            mcode.append(f"    {component} ")
            mcode.append(f"    class {component} pink;")
    mcode.append("    end")
    mcode.append("    class Components blue;")
    #reward_cubesat = rewards["score"]["r_cubesat"]
    mcode.append(f"     {system_class} --- Subsystems")
    for key, value in hierarchy[system_class].items():
        if key.lower() in enabled_systems:
            #reward_subsystem = rewards["score"][key_map[key]]
            for component in value:
                if component in enabled_systems:
                    #reward_component = rewards["score"][key_map[component]]
                    mcode.append(f"     {key} --- {component}")
                    #mcode.append(f"     {key} --{key_map[component]}={reward_component}--- {component}")
    return "\n".join(mcode)