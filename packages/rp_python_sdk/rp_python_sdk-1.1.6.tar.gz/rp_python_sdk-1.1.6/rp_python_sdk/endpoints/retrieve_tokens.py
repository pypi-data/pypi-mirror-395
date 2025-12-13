import base64
import json
import time
import uuid
from typing import Tuple, Any

import requests
from authlib.jose import JsonWebToken
from authlib.jose.errors import BadSignatureError, DecodeError
from authlib.jose.util import extract_header
from joserfc import jws
from joserfc.jwk import RSAKey
from joserfc.jws import JWSRegistry

from rp_python_sdk.endpoints.get_participants import get_issuer_metadata, \
    get_auth_server_details
from rp_python_sdk.endpoints.user_info import call_user_info
from rp_python_sdk.endpoints.util.fapi import create_x_fapi_interaction_id, log_x_fapi_interaction_id_matches
from rp_python_sdk.endpoints.util.mapping import from_dict
from rp_python_sdk.model import CallbackBody, TokenSet, TokenInput, IssuerMetadata
from rp_python_sdk.relying_party_client_sdk_exception import RelyingPartyClientSdkException
from rp_python_sdk.sdk_config import SdkConfig
from rp_python_sdk.setup_logger import logger


def retrieve_tokens(config: SdkConfig, authorisation_server_id: str, callback_body: CallbackBody,
                    original_code_verifier: str,
                    original_state: str, nonce: str) -> TokenSet:
    authorisation_server = get_auth_server_details(config, authorisation_server_id)
    issuer_metadata = get_issuer_metadata(authorisation_server)

    if issuer_metadata.issuer != callback_body.iss:
        raise RelyingPartyClientSdkException(
            f"Issuer returned from authorization endpoint ({callback_body.iss} does not match issuer defined "
            f"in authorization server well-known ({issuer_metadata.issuer})")

    x_fapi_interaction_id = create_x_fapi_interaction_id()
    logger.info(
        f"Retrieving token response from authorisation server: {authorisation_server_id} - "
        f"{authorisation_server.customer_friendly_name}, x-fapi-interaction-id: {x_fapi_interaction_id}")

    token_endpoint = issuer_metadata.get_preferred_token_endpoint()
    issuer = issuer_metadata.issuer

    if callback_body.state != original_state:
        raise RelyingPartyClientSdkException(
            f"Callback response state value does not match state, callback state: {callback_body.state}, "
            f"state {original_state}, x-fapi-interaction-id: {x_fapi_interaction_id}")

    if callback_body.iss != issuer:
        raise RelyingPartyClientSdkException(
            f"iss mismatch, expected {issuer}, got: {callback_body.iss}")

    redirect_uri = config.application_redirect_uri
    client_id = config.client_id
    current_time_in_seconds = int(time.time())
    iat = current_time_in_seconds
    exp = current_time_in_seconds + 300
    jti = str(uuid.uuid4())

    client_assertion_payload = {
        'sub': client_id,
        'aud': issuer,
        'iss': client_id,
        'exp': exp,
        'jti': jti,
        'iat': iat,
    }

    # See https://jose.authlib.org/en/guide/registry/
    registry = JWSRegistry(algorithms=["PS256"])

    key = RSAKey.import_key(config.signing_key)
    header = {'alg': 'PS256', 'kid': config.signing_kid}
    client_assertion_jwt = jws.serialize_compact(header, json.dumps(client_assertion_payload), key, registry=registry)

    # Data payload
    data = {
        "grant_type": "authorization_code",
        "code": callback_body.code,
        "redirect_uri": redirect_uri,
        "client_assertion": client_assertion_jwt,
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "code_verifier": original_code_verifier
    }

    # Custom headers
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": x_fapi_interaction_id
    }

    # Making the POST request
    response = requests.post(token_endpoint, data=data, headers=headers,
                             cert=(config.transport_pem, config.transport_key),
                             verify=config.ca_pem)

    log_x_fapi_interaction_id_matches(authorisation_server, "retrieve_tokens", x_fapi_interaction_id, response)

    if not response.ok:
        raise RelyingPartyClientSdkException(
            f"Response code for token endpoint to {token_endpoint} not successful, was: {response.status_code}, "
            f"x-fapi-interaction-id: {x_fapi_interaction_id}, response body: " + response.text)

    token_input = from_dict(TokenInput, json.loads(response.text))

    jwks_response_body = _get_jwks_json(issuer_metadata, x_fapi_interaction_id)
    allowed_algs = issuer_metadata.id_token_signing_alg_values_supported

    header, payload = _validate(token_input, jwks_response_body, allowed_algs, nonce, client_id, callback_body,
                                issuer_metadata.issuer)

    token_set = TokenSet(token_input, payload, x_fapi_interaction_id)

    if config.custom_config.enable_auto_compliance_verification:
        call_user_info(config, authorisation_server_id, token_set.token_input.access_token)

    logger.info(
        f"Token response successfully retrieved from authorisation server {authorisation_server_id}, "
        f"x-fapi-interaction-id: {x_fapi_interaction_id}, txn: {token_set.claims['txn']}")

    return token_set


def _validate(token_input: TokenInput, jwks_response_body: dict[str, Any], allowed_algs: list[str],
              nonce: str, client_id: str,
              callback_body: CallbackBody, issuer: str) -> Tuple[dict[str, Any], dict[str, Any]]:
    """
    Decode and parse an ID token into JSON objects for header and payload.

    :param token_input: A dictionary containing an 'idToken' key, which is a Base64 encoded string
    :param jwks_response_body
    :param allowed_algs
    :param nonce
    :param client_id
    :param callback_body
    :param issuer
    :return: two dictionaries for header and payload
    """
    id_token = token_input.id_token
    header_json = _get_unverified_header(id_token)

    payload_base64 = id_token.split('.')[1]
    payload = _decode_base64(payload_base64)
    payload_json = json.loads(payload)

    _validate_header(header_json, allowed_algs)
    _validate_signature(issuer, client_id, allowed_algs, id_token, jwks_response_body)
    _validate_payload(payload_json, nonce, callback_body, client_id)

    return header_json, payload_json


def _validate_payload(json_payload: dict[str, Any], nonce: str, callback_body: CallbackBody,
                      client_id: str) -> None:
    if 'nonce' not in json_payload:
        raise RelyingPartyClientSdkException('nonce claim missing from token response')

    if json_payload['nonce'] != nonce:
        raise RelyingPartyClientSdkException(
            f"nonce returned in ID token: {json_payload['nonce']} does not match provided nonce: {nonce}")

    current_time_stamp = int(time.time())

    if 'iss' not in json_payload:
        raise RelyingPartyClientSdkException('iss claim missing from token response')

    if 'iat' not in json_payload:
        raise RelyingPartyClientSdkException('iat claim missing from token response')

    if 'aud' not in json_payload:
        raise RelyingPartyClientSdkException('aud claim missing from token response')

    if 'exp' not in json_payload:
        raise RelyingPartyClientSdkException('exp claim missing from token response')

    # Check if iat claim is older than 10 minutes ago
    if json_payload['iat'] < current_time_stamp - 600:
        raise RelyingPartyClientSdkException('iat claim in token response is too old')

    # Check exp claim is older than current epoch (allowing for 5 minute skew)
    if json_payload['exp'] < current_time_stamp - 300:
        raise RelyingPartyClientSdkException('id token expired more than 5 minutes ago')

    # Check the iss claim is valid
    if json_payload['iss'] != callback_body.iss:
        raise RelyingPartyClientSdkException(
            f'iss claim in token response "{json_payload["iss"]}" does not match '
            f'the expected value of "{callback_body.iss}"')

    # Extract aud claim from either list or string
    if isinstance(json_payload['aud'], list):
        for aud_element in json_payload['aud']:
            if aud_element != client_id:
                raise RelyingPartyClientSdkException(
                    'one of the aud claim elements in token response does not match client ID')
    else:
        if json_payload['aud'] != client_id:
            raise RelyingPartyClientSdkException('aud claim in token response does not match client ID')


def _get_unverified_header(id_token: str) -> Any:
    return extract_header(id_token.split('.')[0].encode(), DecodeError)


def _decode_base64(base64_str: str) -> str:
    """
    Decode a Base64 encoded string.
    :param base64_str: Base64 encoded string
    :return: decoded string
    """
    decoded_bytes = base64.b64decode(base64_str + '==')
    return decoded_bytes.decode('utf-8')


def _validate_header(json_header: dict, allowed_algs: list) -> None:
    if 'alg' not in json_header or json_header['alg'] == 'none':
        raise RelyingPartyClientSdkException("no alg value in the token response jwt header")

    if 'kid' not in json_header:
        raise RelyingPartyClientSdkException("no kid value in the token response jwt header")

    found_alg = any(alg.lower() == json_header['alg'].lower() for alg in allowed_algs)
    if not found_alg:
        raise RelyingPartyClientSdkException(
            f"alg value in id token header is not one of the supported algorithms listed on the well-known. "
            f"Provided alg {json_header['alg']}")


def _find_key_in_jwks(kid: str, token_alg: str, jwks: dict) -> Any:
    for key_element in jwks.get('keys', []):
        if _matching_kid(kid, key_element) and _matching_alg(token_alg, key_element) and _matching_use(key_element):
            return key_element
    return None


def _validate_signature(issuer: str, audience: str, allowed_alg: list, id_token: str, jwks: dict) -> None:
    try:
        # Pub key extraction
        header = _get_unverified_header(id_token)
        kid = header['kid']
        alg = header['alg']
        jwk = _find_key_in_jwks(kid, alg, jwks)

        if jwk is None:
            raise RelyingPartyClientSdkException(
                f"kid and alg provided does not match any key in the jwks for specified algorithm in "
                f"token header, kid: {kid}, alg: {alg}")

        # Decode JWT with signature verification
        claims_options = {
            "iss": {"essential": True, "value": issuer},
            "aud": {"essential": True, "value": audience}
        }
        jwt = JsonWebToken(allowed_alg)
        claims = jwt.decode(id_token, key=jwk, claims_options=claims_options)
        claims.validate()
        logger.info("JWT signature is valid")
    except BadSignatureError as e:
        raise RelyingPartyClientSdkException(f"Invalid JWT signature: {e}, token data: {e.result}")
    except Exception as e:
        logger.debug(f"Invalid JWT token: {id_token}")
        raise RelyingPartyClientSdkException(f"Invalid JWT signature: {e}")


def _matching_use(key_element: dict) -> bool:
    return key_element.get('use') == "sig"


def _matching_kid(kid: str, key_element: dict) -> bool:
    return key_element.get('kid') == kid


def _matching_alg(token_alg: str, key_element: dict) -> bool:
    return key_element.get("alg") is None or key_element.get("alg") == token_alg


def _get_jwks_json(issuer_metadata: IssuerMetadata, x_fapi_interaction_id: str) -> Any:
    headers = {
        "Accept": "application/json",
        "x-fapi-interaction-id": x_fapi_interaction_id
    }
    response = requests.get(issuer_metadata.jwks_uri, headers=headers)
    response.raise_for_status()

    if not response.ok:
        raise RelyingPartyClientSdkException(
            f"Response code for JWKS to {issuer_metadata.jwks_uri} not successful, was: {response.status_code}, "
            f"x-fapi-interaction-id: {x_fapi_interaction_id}, response body: {response.text}")

    return response.json()
