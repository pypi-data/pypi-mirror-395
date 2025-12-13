from typing import Any

import requests

from rp_python_sdk.endpoints.get_participants import get_issuer_metadata, \
    get_auth_server_details
from rp_python_sdk.endpoints.util.fapi import create_x_fapi_interaction_id
from rp_python_sdk.relying_party_client_sdk_exception import RelyingPartyClientSdkException
from rp_python_sdk.sdk_config import SdkConfig
from rp_python_sdk.setup_logger import logger


def call_user_info(config: SdkConfig, authorisation_server_id: str, access_token: str) -> dict[str, Any]:
    x_fapi_interaction_id = create_x_fapi_interaction_id()
    logger.info(f"Making call to user info endpoint, x-fapi-interaction-id: {x_fapi_interaction_id}")

    authorisation_server = get_auth_server_details(config, authorisation_server_id)
    issuer_metadata = get_issuer_metadata(authorisation_server)

    user_info_endpoint = issuer_metadata.get_preferred_userinfo_endpoint()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-fapi-interaction-id": x_fapi_interaction_id
    }

    try:
        response = requests.get(user_info_endpoint, headers=headers,
                                cert=(config.transport_pem, config.transport_key),
                                verify=config.ca_pem)

        if not _is_success(response):
            raise RelyingPartyClientSdkException(
                f"Call to user info endpoint failed with code: {response.status_code}")

        return response.json()

    except requests.exceptions.RequestException as e:
        raise RelyingPartyClientSdkException(
            f"Failed to read body from response while connecting to {user_info_endpoint}") from e


def _is_success(response: requests.Response) -> bool:
    return 200 <= response.status_code < 300
