import inspect
import os
import time
import warnings
from pathlib import Path

import httpx
import streamlit as st
import toml
from deprecated import deprecated

from .logging_setup import logger_ai4cehelper


def warn_if_external_call():
    frame = inspect.currentframe()
    caller_frame = frame.f_back.f_back  # skip: warn_if_external_call -> _backend_GET -> caller
    
    caller_module = inspect.getmodule(caller_frame)
    external_function_name = caller_frame.f_code.co_name
    internal_function_name = frame.f_back.f_code.co_name

    if caller_module and not caller_module.__name__.startswith("ai4ce_helpers"):
        logger_ai4cehelper.warning(
            f"(wiec) Function '{external_function_name}' is calling internal backend function '{internal_function_name}' which"
            " handles errors internally and always returns "
            "(status_code, data/error_message). Make sure to handle these values."
        )
        warnings.warn(
            f"Function '{external_function_name}' is calling internal backend function '{internal_function_name}' which"
            " handles errors internally and always returns "
            "(status_code, data/error_message). Make sure to handle these values.",
            UserWarning,
            stacklevel=3,
        )


# Set backend base url, depending on whether the app is running in
# a docker container (which is most likely the unified interface.)
def check_if_backend_in_docker(PORT: int = 8000) -> str:
    """Check if the backend is running in a Docker container.
    If streamlit is started as part of docker, it will most likely have an environment variable set for the backend URL.
    If not, the backend is assumed to be running on localhost.

    Args:
        PORT (int): The port on which the backend is running.
    Returns:
        str: The URL of the backend.
    """
    if os.environ.get("BACKEND_URL"):
        logger_ai4cehelper.info(f"(cibid) Using BACKEND_URL from environment: {os.environ.get('BACKEND_URL')}")
        return f"{os.environ.get('BACKEND_URL')}"
    if Path("/.dockerenv").exists():
        logger_ai4cehelper.info(f"(cibid) Detected Docker environment. Using backend URL: http://backend:{PORT}")
        return f"http://backend:{PORT}"
    logger_ai4cehelper.warning(
        f"(cibid) Neither BACKEND_URL env variable nor Docker environment detected. Using localhost backend URL: http://localhost:{PORT}"
    )
    return f"http://localhost:{PORT}"


BACKEND_URL = check_if_backend_in_docker()


def check_backend_availability():
    """Check check every 5 seconds if the backend is available.
    Wait a max of 30 seconds before giving up. Display loading message
    during check, remove loading message once backend is available. Display
    error message if backend is not available.

    Check the session state to see if the backend is already available.
    If it is, do not check again.
    """
    logger_ai4cehelper.info("(cba) Checking backend availability...")
    backend_available = False
    timeout = 30

    backend_url = check_if_backend_in_docker().removesuffix("/api")

    # check if backend is already available
    if "backend_available" in st.session_state:
        backend_available = st.session_state.backend_available

    # display loading message
    checking = st.warning("Waiting for backend...")
    while not backend_available and timeout > 0:
        # check if backend is available
        # If it is, set backend_available to True and remove the loading message
        try:
            httpx.get(backend_url, timeout=1)
            backend_available = True

        except (httpx.TimeoutException, httpx.ConnectError, httpx.RemoteProtocolError):
            logger_ai4cehelper.debug(f"(cba) Backend not available yet at {backend_url}, retrying in 5 seconds...")
            time.sleep(5)
            st.session_state.backend_available = False

        timeout -= 5
        
    response = httpx.get(f"{backend_url}/api/v2/status/healthcheck", timeout=1)
    logger_ai4cehelper.debug(f"(cba) Exited backend availability check loop with backend_available={backend_available} and timeout={timeout}s")
    if not backend_available:
        logger_ai4cehelper.error(f"(cba) Backend is not available at {backend_url}")
        checking.empty()
        st.error(f"Backend is not available at {backend_url}")
        st.session_state.backend_available = False
        return
    else:
        if response is not None:
            if response.status_code != 200:
                logger_ai4cehelper.error(f"(cba) Backend returned status code {response.status_code} at {backend_url}")
                st.error(f"Backend returned status code {response.status_code} at {backend_url}")
                st.session_state.backend_available = False
            else:
                # remove loading message
                logger_ai4cehelper.info(f"(cba) Backend is available at {backend_url}")
                checking.empty()
                logger_ai4cehelper.info(f"(cba) Removing loading message.")
                st.session_state.backend_available = True
    


@st.cache_data(ttl=300)
def get_running_backend_version() -> str:
    """Get the latest version of the backend from the openapi.json file."""
    status_code, response = _backend_GET("/openapi.json")
    if status_code == 200 and isinstance(response, dict) and "info" in response and "version" in response["info"]:
        version = response["info"]["version"]
        if "a" in version:
            version = version.split("a")[0] + " (alpha" + version.split("a")[1] + ")"
        if "b" in version:
            version = version.split("b")[0] + " (beta" + version.split("b")[1] + ")"
        if "rc" in version:
            version = version.split("rc")[0] + " (rc" + version.split("rc")[1] + ")"
        logger_ai4cehelper.info(f"(g_rbv) Retrieved backend version: {version}")
        return version
    logger_ai4cehelper.error("(g_rbv) Could not retrieve backend version.")
    return "unknown"


api_excluded_endpoints = ["/requestpid", "/openapi.json"]


@deprecated(
    reason="This function is deprecated. Please use _backend_GET() instead.",
    category=DeprecationWarning,
)
def _backend_get(endpoint: str) -> dict | str:
    """Deprecated: use _backend_GET() instead."""
    warnings.warn(
        "This function is deprecated. Please use _backend_GET() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    logger_ai4cehelper.warning("(bc) _backend_get is deprecated. Use _backend_GET instead.")
    warn_if_external_call()
    return _backend_GET(endpoint=endpoint)[1]


def _backend_GET(
    endpoint: str,
    query_params: dict | None = None,
    headers: dict = {"accept": "application/json, application/toml"},
) -> tuple[int, dict | list | str]:
    """An internal function to make the development of get functions easier.

    Params:
        endpoint(str): the URL of the backend endpoint to post to

    Returns:
        dict: json response from the backend
    """
    warn_if_external_call()
    endpoint = f"/api{endpoint}" if endpoint not in api_excluded_endpoints else endpoint

    try:
        response = httpx.get(
            url=f"{BACKEND_URL}{endpoint}",
            headers=headers,
            follow_redirects=True,
            params=query_params,
        )

        # Raises an HTTPError if the response status code is 4xx or 5xx
        response.raise_for_status()
        if response.status_code == 200:
            return (
                response.status_code,
                (
                    toml.loads(response.text)
                    if response.headers["content-type"] == "application/toml"
                    else response.json()
                ),
            )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            logger_ai4cehelper.error(f"(bc) Server Error (500):{e.response.text}")
            return (
                e.response.status_code,
                "Server Error: 500. Please check the logs for details",
            )
        elif e.response.status_code == 422:
            logger_ai4cehelper.error(f"(bc) Unprocessable Content (422): {e.response.text}")
            return (
                e.response.status_code,
                "A problem with the payload itself has been detected. Please check the logs for details.",
            )
        else:
            logger_ai4cehelper.error(f"(bc) Error ({e.response.status_code}): {e.response.text}")
            return (e.response.status_code, e.response.json())
    except (httpx.RequestError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
        logger_ai4cehelper.error(f"(bc) An error occurred while requesting {e.request.url!r}.")
        return (500, f"Request Error: {e}")
    return (500, "An unknown error occurred.")


@deprecated(
    reason="This function is deprecated. Please use _backend_POST() instead.",
    category=DeprecationWarning,
)
def _backend_post(endpoint: str, data: dict) -> tuple[int, dict | str]:
    """This function is deprecated. Please use _backend_POST() instead."""
    warnings.warn(
        "This function is deprecated. Please use _backend_POST() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    logger_ai4cehelper.warning("(bc) _backend_post is deprecated. Use _backend_POST instead.")
    warn_if_external_call()
    return _backend_POST(endpoint=endpoint, data=data)


def _backend_POST(
    endpoint: str,
    data: dict,
    query_params: dict | None = None,
    headers: dict = {"Content-Type": "application/json", "accept": "application/json"},
) -> tuple[int, dict | list | str]:
    """An internal function to make the development of posting functions easier.

    Params:
        endpoint(str): the URL of the backend endpoint to post to
        data(dict): the concent to put into the backend

    Returns:
        dict: json response from the backend

    Catches:
        httpx.HTTPStatusError: if the response status code is 4xx or 5xx
        httpx.RequestError: if there is a problem with the request
    """
    warn_if_external_call()
    endpoint = f"/api{endpoint}" if endpoint not in api_excluded_endpoints else endpoint

    # Make the POST request
    try:
        response = httpx.post(
            url=f"{BACKEND_URL}{endpoint}",
            json=data,
            headers=headers,
            follow_redirects=True,
            params=query_params,
        )
        response.raise_for_status()
        if response.status_code == 201:
            return (response.status_code, response.json())
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            logger_ai4cehelper.error(f"(bp) Server Error (500):{e.response.text}")
            return (
                e.response.status_code,
                "Server Error: 500. Please check the logs for details",
            )
        elif e.response.status_code == 422:
            logger_ai4cehelper.error(f"(bp) Unprocessable Content (422): {e.response.text}")
            return (
                e.response.status_code,
                "A problem with the payload itself has been detected. Please check the logs for details.",
            )
        else:
            logger_ai4cehelper.error(f"(bp) Error ({e.response.status_code}): {e.response.text}")
            return (e.response.status_code, e.response.json())
    except (httpx.RequestError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
        logger_ai4cehelper.error(f"(bp) An error occurred while requesting {e.request.url!r}.")
        return (500, f"Request Error: {e}")
    return (500, "An unknown error occurred.")


@deprecated(
    reason="This function is deprecated. Please use _backend_PUT() instead.",
    category=DeprecationWarning,
)
def _backend_put(endpoint: str, data: dict) -> tuple[int, dict | str]:
    """This function is deprecated. Please use _backend_PUT() instead."""
    warnings.warn(
        "This function is deprecated. Please use _backend_PUT() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    logger_ai4cehelper.warning("(bc) _backend_put is deprecated. Use _backend_PUT instead.")
    warn_if_external_call()
    return _backend_PUT(endpoint=endpoint, data=data)


def _backend_PUT(
    endpoint: str,
    data: dict,
    query_params: dict | None = None,
    headers: dict = {"Content-Type": "application/json", "accept": "application/json"},
) -> tuple[int, dict | list | str]:
    """An internal function to make the development of PUT functions/update easier.

    Params:
        endpoint(str): the URL of the backend endpoint to post to
        data(dict): the concent to put into the backend
        headers(dict | None): headers to include in the request

    Returns:
        dict: response from the backend
    """
    warn_if_external_call()
    endpoint = f"/api{endpoint}" if endpoint not in api_excluded_endpoints else endpoint

    # Make the PUT request
    try:
        response = httpx.put(
            url=f"{BACKEND_URL}{endpoint}",
            json=data,
            headers=headers,
            follow_redirects=True,
            params=query_params,
        )
        response.raise_for_status()
        if response.status_code == 200:
            return (
                response.status_code,
                (
                    toml.loads(response.text)
                    if response.headers["content-type"] == "application/toml"
                    else response.json()
                ),
            )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            logger_ai4cehelper.error(f"(bput) Server Error (500):{e.response.text}")
            return (
                e.response.status_code,
                "Server Error: 500. Please check the logs for details",
            )
        elif e.response.status_code == 422:
            logger_ai4cehelper.error(f"(bput) Unprocessable Content (422): {e.response.text}")
            return (
                e.response.status_code,
                "A problem with the payload itself has been detected. Please check the logs for details.",
            )
        else:
            logger_ai4cehelper.error(f"(bput) Error ({e.response.status_code}): {e.response.text}")
            return (e.response.status_code, e.response.json())
    except (httpx.RequestError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
        logger_ai4cehelper.error(f"(bput) An error occurred while requesting {e.request.url!r}.")
        return (500, f"Request Error: {e}")
    return (500, "An unknown error occurred.")
