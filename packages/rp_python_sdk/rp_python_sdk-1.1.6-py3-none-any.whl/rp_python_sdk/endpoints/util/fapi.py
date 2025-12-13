import uuid

from requests.models import Response

from rp_python_sdk.model import AuthorisationServer
from rp_python_sdk.setup_logger import logger


def create_x_fapi_interaction_id() -> str:
    return str(uuid.uuid4())


def log_x_fapi_interaction_id_matches(authorisation_server: AuthorisationServer, request_name: str,
                                      x_fapi_interaction_id: str, response: Response) -> None:
    fapi_header = response.headers.get('x-fapi-interaction-id')
    if not fapi_header:
        logger.warning(
            f"No x-fapi-interaction-id header returned from auth server {authorisation_server.authorisation_server_id} "
            f"on request {request_name}, expected {x_fapi_interaction_id}")
        return
    elif x_fapi_interaction_id == fapi_header:
        logger.debug(
            f"x-fapi-interaction-id correctly returned from auth server {authorisation_server.authorisation_server_id} "
            f"on {request_name} matched expected {x_fapi_interaction_id}")
        return
    else:
        logger.warning(
            f"x-fapi-interaction-id returned from auth server {authorisation_server.authorisation_server_id} "
            f"on {request_name} did not match. sent {x_fapi_interaction_id}, returned {fapi_header}")
