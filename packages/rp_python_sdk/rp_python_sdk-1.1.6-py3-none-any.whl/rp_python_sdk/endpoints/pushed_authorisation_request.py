import json
import time
import uuid
from typing import Any
from urllib.parse import quote

import requests
from authlib.common.security import generate_token
from authlib.jose import JsonWebSignature
from authlib.oauth2.rfc7636 import create_s256_code_challenge

from rp_python_sdk.endpoints.get_participants import get_auth_server_details, \
    get_issuer_metadata
from rp_python_sdk.endpoints.util.fapi import create_x_fapi_interaction_id, log_x_fapi_interaction_id_matches
from rp_python_sdk.model import PARResponse
from rp_python_sdk.relying_party_client_sdk_exception import RelyingPartyClientSdkException
from rp_python_sdk.sdk_config import SdkConfig
from rp_python_sdk.setup_logger import logger

extended_claims = {"over16", "over18", "over21", "over25", "over65", "beneficiary_account_au",
                   "beneficiary_account_au_payid", "beneficiary_account_international"}


def send_pushed_authorisation_request(config: SdkConfig,
                                      authorisation_server_id: str,
                                      essential_claims: set[str],
                                      voluntary_claims: set[str],
                                      purpose: str) -> PARResponse:
    _check_valid_purpose(purpose)

    checked_essential_claims = _ensure_mandatory_claims_present(essential_claims, voluntary_claims)
    claim_request = _generate_claims_request(checked_essential_claims, voluntary_claims)

    authorisation_server = get_auth_server_details(config, authorisation_server_id)
    issuer_metadata = get_issuer_metadata(authorisation_server)

    auth_server_url = issuer_metadata.issuer
    x_fapi_interaction_id = create_x_fapi_interaction_id()

    logger.info(
        f"Sending PAR to auth server: {authorisation_server_id} - {authorisation_server.customer_friendly_name}, "
        f"essential claims requested: {checked_essential_claims}, voluntary claims requested: {voluntary_claims}, "
        f"x-fapi-interaction-id: {x_fapi_interaction_id}, purpose: {purpose}")

    par_endpoint = issuer_metadata.get_preferred_pushed_authorization_request_endpoint()
    auth_endpoint = issuer_metadata.get_preferred_authorization_endpoint()
    redirect_uri = config.application_redirect_uri
    client_id = config.client_id

    current_time_in_seconds = int(time.time())

    iat = current_time_in_seconds
    exp = current_time_in_seconds + 300

    state = generate_token()
    nonce = generate_token()
    scope = "openid"
    jti = str(uuid.uuid4())

    code_verifier = generate_token(48)
    code_challenge = create_s256_code_challenge(code_verifier)

    header = {'alg': 'PS256', 'kid': config.signing_kid}
    request_payload = {
        'iss': client_id,
        'aud': auth_server_url,
        'exp': exp,
        'nbf': iat,
        'response_type': 'code',
        'code_challenge_method': 'S256',
        'nonce': nonce,
        'client_id': client_id,
        'scope': scope,
        'claims': claim_request,
        'redirect_uri': redirect_uri,
        'state': state,
        'prompt': 'consent',
        'code_challenge': code_challenge,
        'purpose': purpose,
    }

    jws = JsonWebSignature()
    request_jwt = jws.serialize_compact(header, json.dumps(request_payload), config.signing_key)

    client_assertion_payload = {
        'sub': client_id,
        'aud': auth_server_url,
        'iss': client_id,
        'exp': exp,
        'jti': jti,
        'iat': iat,
    }

    client_assertion_jwt = jws.serialize_compact(header, json.dumps(client_assertion_payload),
                                                 config.signing_key)

    # Data payload
    data = {
        "request": request_jwt.decode("utf-8"),
        "client_assertion": client_assertion_jwt.decode("utf-8"),
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
    }

    # Custom headers
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": x_fapi_interaction_id
    }

    # Making the POST request
    response = requests.post(par_endpoint, data=data, headers=headers,
                             cert=(config.transport_pem, config.transport_key),
                             verify=config.ca_pem)

    log_x_fapi_interaction_id_matches(authorisation_server, "send_pushed_authorisation_request",
                                      x_fapi_interaction_id, response)

    if not response.ok:
        raise RelyingPartyClientSdkException(f"Response code for PAR to {authorisation_server_id} not successful, "
                                             f"was: {response.status_code} x-fapi-interaction-id: {x_fapi_interaction_id}")

    request_uri = response.json()['request_uri']
    logger.debug(f"PAR was sent, request_uri='{request_uri}'")

    return PARResponse(_construct_auth_url(auth_endpoint, client_id, request_uri),
                       code_verifier, state, nonce, x_fapi_interaction_id)


def _check_valid_purpose(purpose: str) -> None:
    if len(purpose) < 3 or len(purpose) > 300:
        raise RelyingPartyClientSdkException("Purpose must be between 3 and 300 characters")

    illegal_chars = ["<", ">", "(", ")", "{", "}", "'", "\\"]

    contains_illegal_char = any(char in purpose for char in illegal_chars)
    if contains_illegal_char:
        raise RelyingPartyClientSdkException(
            f"Purpose cannot contain any of the following characters: {', '.join(illegal_chars)}, "
            f"purpose supplied: [{purpose}]")


def _ensure_mandatory_claims_present(essential_claims: set[str], voluntary_claims: set[str]) -> set[str]:
    if "txn" in essential_claims or "txn" in voluntary_claims:
        return essential_claims

    # Create a copy of the essential_claims to avoid modifying the original set
    result_claims = essential_claims.copy()
    # Add "txn" to the set
    result_claims.add("txn")
    return result_claims


def _generate_claims_request(essential_claims: set[str], voluntary_claims: set[str]) -> dict[str, Any]:
    # Filter out any claims that are in both essential and voluntary sets so essential takes precedence
    deduplicated_voluntary_claims = voluntary_claims - essential_claims

    # Create maps for essential and voluntary claims
    essential = {"essential": True}
    voluntary = {"essential": False}

    # Partition claims into basic and extended types
    partitioned_essential_claims = _partition_claims(essential_claims)
    partitioned_voluntary_claims = _partition_claims(deduplicated_voluntary_claims)

    # Map basic claims to their respective maps
    id_token_claims = _map_claims(partitioned_essential_claims[False], essential)
    id_token_claims.update(_map_claims(partitioned_voluntary_claims[False], voluntary))

    # Map extended claims to their respective maps
    extended_claims = _map_claims(partitioned_essential_claims[True], essential)
    extended_claims.update(_map_claims(partitioned_voluntary_claims[True], voluntary))

    # Add extended claims to idTokenClaims if any exist
    if extended_claims:
        id_token_claims["verified_claims"] = {
            "verification": {"trust_framework": {"value": "au_connectid"}},
            "claims": extended_claims
        }

    return {"id_token": id_token_claims}


def _partition_claims(claims: set[str]) -> dict[bool, set[str]]:
    """
    Partition claims into basic and extended types based on a criteria (here, whether they are in extended_claims).
    """
    partitioned: dict[bool, set[str]] = {True: set(), False: set()}
    for claim in claims:
        partitioned[claim in extended_claims].add(claim)
    return partitioned


def _map_claims(claims: set[str], claim_map: dict[str, Any]) -> dict[str, Any]:
    """
    Map each claim to the provided claim_map.
    """
    return {claim: claim_map for claim in claims}


def _construct_auth_url(auth_endpoint: str, client_id: str, request_uri: str) -> str:
    return (
        f"{auth_endpoint}"
        f"?client_id={quote(client_id)}"
        f"&request_uri={quote(request_uri)}"
    )
