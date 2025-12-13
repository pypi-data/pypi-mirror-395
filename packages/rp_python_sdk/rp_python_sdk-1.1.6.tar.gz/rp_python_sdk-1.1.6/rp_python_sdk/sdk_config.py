from dataclasses import dataclass, field
from typing import Any, List
from urllib.parse import urlparse

from rp_python_sdk.setup_logger import logger


def assert_not_blank(value: str, parameter_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{parameter_name} can't be blank")


def assert_not_null(value: Any, parameter_name: str) -> None:
    if value is None:
        raise ValueError(f"{parameter_name} can't be null")


@dataclass
class CustomConfig:
    enable_auto_compliance_verification: bool = False
    purpose: str = "verifying your identity"
    include_uncertified_participants: bool = False
    required_claims: List[str] = field(default_factory=list)
    required_participant_certifications: List['CertificationFilter'] = field(default_factory=list)
    timeout_in_seconds: int = 10

    def __post_init__(self) -> None:
        if self.include_uncertified_participants:
            logger.info("Identity provider list will not be filtered as includeUncertifiedParticipants=true")
        else:
            if self.required_claims:
                logger.info(
                    f"Identity provider list will be filtered for participants "
                    f"that support the following claims: {self.required_claims}")
            if self.required_participant_certifications:
                logger.info(
                    f"Identity provider list will be filtered for participants "
                    f"that support the following certifications: {self.required_participant_certifications}")


@dataclass
class SdkConfig:
    signing_kid: str
    transport_key: str
    transport_pem: str
    signing_key: str
    signing_pem: str
    ca_pem: str
    application_redirect_uri: str
    registry_participants_uri: str
    client_id: str
    custom_config: CustomConfig  # TODO: fix this = field(default_factory=lambda: CustomConfig())

    def __post_init__(self) -> None:
        assert_not_blank(self.signing_kid, "Signing kid")
        assert_not_blank(self.transport_key, "Transport key")
        assert_not_blank(self.transport_pem, "Transport pem")
        assert_not_blank(self.signing_key, "Signing key")
        assert_not_blank(self.signing_pem, "Signing pem")
        assert_not_blank(self.ca_pem, "CA pem")

        # For URI validation, we're using urlparse
        for uri_attr in ['application_redirect_uri', 'registry_participants_uri', 'client_id']:
            uri_value = getattr(self, uri_attr)
            assert_not_null(urlparse(uri_value).scheme, uri_attr)  # Simple check to ensure it's a valid URI


@dataclass
class CertificationFilter:
    profile_variant: str
    profile_type: str

    def __str__(self) -> str:
        return f"CertificationFilter{{profileVariant='{self.profile_variant}', profileType='{self.profile_type}'}}"
