import json
from datetime import date

import requests

from rp_python_sdk.endpoints.util.mapping import from_dict
from rp_python_sdk.endpoints.util.user_agent import build_user_agent
from rp_python_sdk.filters.participant_filters import remove_out_of_date_certifications, \
    remove_unofficial_certifications, filter_for_fallback_identity_service_providers, \
    remove_participants_without_auth_servers, remove_fallback_identity_service_provider, \
    filter_auth_servers_for_supported_claims, filter_for_required_certifications, remove_inactive_auth_servers
from rp_python_sdk.model import IssuerMetadata, AuthorisationServer
from rp_python_sdk.model import Participant
from rp_python_sdk.relying_party_client_sdk_exception import RelyingPartyClientSdkException
from rp_python_sdk.sdk_config import SdkConfig
from rp_python_sdk.setup_logger import logger


def get_participants(config: SdkConfig) -> list[Participant]:
    participants = _retrieve_full_participants_list(config)

    filtered_participants = remove_fallback_identity_service_provider(participants)

    if config.custom_config.include_uncertified_participants:
        logger.info("Identity provider list has not been filtered as includeUncertifiedParticipants=true")
        filtered_participants = remove_participants_without_auth_servers(filtered_participants)
        return filtered_participants

    filtered_participants = remove_out_of_date_certifications(filtered_participants, date.today())
    filtered_participants = remove_unofficial_certifications(filtered_participants)

    if len(config.custom_config.required_claims) != 0:
        logger.debug(f"Identity provider list filtered for participants that support the "
                     f"following claims: {config.custom_config.required_claims}")
        filtered_participants = filter_auth_servers_for_supported_claims(filtered_participants,
                                                                         config.custom_config.required_claims)

    if len(config.custom_config.required_participant_certifications) != 0:
        logger.debug(f"Identity provider list filtered for participants that support the "
                     f"following certifications: {config.custom_config.required_participant_certifications}")
        filtered_participants = filter_for_required_certifications(filtered_participants,
                                                                   config.custom_config.required_participant_certifications)

    filtered_participants = remove_inactive_auth_servers(filtered_participants)
    filtered_participants = remove_participants_without_auth_servers(filtered_participants)

    return filtered_participants


def retrieve_fallback_provider_participants(config: SdkConfig) -> list[Participant]:
    participants = _retrieve_full_participants_list(config)

    filtered_participants = remove_out_of_date_certifications(participants, date.today())
    filtered_participants = remove_unofficial_certifications(filtered_participants)

    filtered_participants = filter_for_fallback_identity_service_providers(filtered_participants)
    filtered_participants = remove_participants_without_auth_servers(filtered_participants)

    return filtered_participants


def _retrieve_full_participants_list(config: SdkConfig) -> list[Participant]:
    logger.info(f"Retrieving all identity providers from {config.registry_participants_uri}")

    response = requests.get(config.registry_participants_uri,
                            timeout=config.custom_config.timeout_in_seconds,
                            headers={
                                'User-Agent': build_user_agent(config.client_id)
                            })
    if response.status_code != 200:
        raise RelyingPartyClientSdkException(
            f"Call to identity provider endpoint failed with code: {response.status_code}")

    # participant_list: list[Participant] = Participant.from_json(response.text)
    participant_list: list[Participant] = from_dict(Participant, json.loads(response.text), pascal_case=True)

    logger.info(f"Retrieved identity providers, num orgs found: {len(participant_list)}")
    return participant_list


def get_auth_server_details(config: SdkConfig, authorisation_server_id: str) -> AuthorisationServer:
    def find_auth_server_by_id(participants: list[Participant], target_id: str) -> AuthorisationServer | None:
        for participant in participants:
            for server in participant.authorisation_servers:
                if str(server.authorisation_server_id) == target_id:
                    return server
        return None

    # Search in main participants
    result = find_auth_server_by_id(get_participants(config), authorisation_server_id)

    # If not found, check fallback provider participants
    if result is None:
        fallback_participants = retrieve_fallback_provider_participants(config)
        result = find_auth_server_by_id(fallback_participants, authorisation_server_id)

    if result is None:
        raise RelyingPartyClientSdkException(
            f"No authorisation server with id: {authorisation_server_id} was found")

    return result


def get_issuer_metadata(authorisation_server: AuthorisationServer) -> IssuerMetadata:
    auth_server_issuer = authorisation_server.open_i_d_discovery_document

    try:
        logger.info(f"Getting discovery document from {auth_server_issuer}")
        response = requests.get(auth_server_issuer)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX errors

        return from_dict(IssuerMetadata, json.loads(response.text))

    except requests.exceptions.HTTPError as http_err:
        raise RelyingPartyClientSdkException(
            f"Call to identity provider endpoint failed with code: {response.status_code}") from http_err
    except requests.exceptions.RequestException as req_err:
        raise RelyingPartyClientSdkException(
            f"Failed to connect to authorisation service {auth_server_issuer}") from req_err
