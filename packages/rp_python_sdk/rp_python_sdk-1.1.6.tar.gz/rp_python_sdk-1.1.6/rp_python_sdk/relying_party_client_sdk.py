from rp_python_sdk.endpoints.get_participants import get_participants, \
    retrieve_fallback_provider_participants
from rp_python_sdk.endpoints.pushed_authorisation_request import send_pushed_authorisation_request
from rp_python_sdk.endpoints.retrieve_tokens import retrieve_tokens

from rp_python_sdk.model import Participant, PARResponse, CallbackBody, TokenSet
from rp_python_sdk.sdk_config import SdkConfig
from rp_python_sdk.setup_logger import logger


class RelyingPartyClientSdk:

    def __init__(self, config: SdkConfig):
        self.config = config

        if config.custom_config.enable_auto_compliance_verification:
            logger.info(f"Auto Compliance Verification mode enabled, printing config information: "
                        f"client_id={self.config.client_id}, "
                        f"signing_kid={self.config.signing_kid}, "
                        f"application_redirect_uri={self.config.application_redirect_uri}, "
                        f"registry_participants_uri={self.config.registry_participants_uri}")

    def get_participants(self) -> list[Participant]:
        return get_participants(self.config)

    def get_fallback_provider_participants(self) -> list[Participant]:
        return retrieve_fallback_provider_participants(self.config)

    def send_pushed_authorisation_request(self, authorisation_server_id: str,
                                          essential_claims: set[str] | None = None,
                                          voluntary_claims: set[str] | None = None,
                                          purpose: str | None = None) -> PARResponse:
        # Converting the claims to a set just in case a non-set (e.g. list) was passed in.
        checked_essential_claims = set(essential_claims) if essential_claims else set()
        checked_voluntary_claims = set(voluntary_claims) if voluntary_claims else set()
        checked_purpose = purpose if purpose else self.config.custom_config.purpose

        return send_pushed_authorisation_request(self.config, authorisation_server_id, checked_essential_claims,
                                                 checked_voluntary_claims, checked_purpose)

    def retrieve_tokens(self, authorisation_server_id: str, callback_body: CallbackBody, original_code_verifier: str,
                        original_state: str, nonce: str) -> TokenSet:
        return retrieve_tokens(self.config, authorisation_server_id, callback_body, original_code_verifier,
                               original_state, nonce)
