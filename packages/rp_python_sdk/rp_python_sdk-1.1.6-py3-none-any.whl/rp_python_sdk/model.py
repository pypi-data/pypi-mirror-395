from dataclasses import dataclass
from typing import Any, Dict, Optional
from typing import List


@dataclass
class Participant:
    organisation_id: str
    status: str
    organisation_name: str
    created_on: str
    legal_entity_name: str
    country_of_registration: str
    company_register: str
    registration_number: str
    registration_id: str
    registered_name: str
    address_line1: str
    address_line2: str
    city: str
    postcode: str
    country: str
    parent_organisation_reference: str
    authorisation_servers: List['AuthorisationServer']  # Use quotes for forward references
    org_domain_claims: List['OrgDomainClaim']
    org_domain_role_claims: List['OrgDomainRoleClaim']


@dataclass
class AuthorisationServerCertification:
    certification_start_date: str  # date
    certification_expiration_date: str  # date
    certification_id: str
    authorisation_server_id: str
    status: str
    profile_variant: str
    profile_type: str
    profile_version: str
    certification_uri: str


@dataclass
class OrgDomainClaim:
    authorisation_domain_name: str
    authority_name: str
    registration_id: str
    status: str


@dataclass
class ApiDiscoveryEndpoint:
    api_discovery_id: str
    api_endpoint: str


@dataclass
class ApiResource:
    api_resource_id: str
    api_version: str
    api_discovery_endpoints: List[ApiDiscoveryEndpoint]
    family_complete: bool
    api_certification_uri: Optional[str]
    certification_status: Optional[str]
    # should be a date
    certification_start_date: str
    # should be a date
    certification_expiration_date: str
    api_family_type: Optional[str]


@dataclass
class AuthorisationServer:
    authorisation_server_id: str
    api_resources: List[ApiResource]
    authorisation_server_certifications: List[AuthorisationServerCertification]
    customer_friendly_description: str
    customer_friendly_logo_uri: str
    customer_friendly_name: str
    developer_portal_uri: str
    terms_of_service_uri: str
    open_i_d_discovery_document: str
    issuer: str
    payload_signing_cert_location_uri: str
    parent_authorisation_server_id: str


@dataclass
class OrgDomainRoleClaim:
    status: str
    authorisation_domain: str
    role: str
    registration_id: str


@dataclass
class CallbackBody:
    code: str
    iss: str
    state: str


@dataclass
class PARResponse:
    auth_url: str
    code_verifier: str
    state: str
    nonce: str
    x_fapi_interaction_id: str


@dataclass
class TokenSet:
    token_input: 'TokenInput'
    claims: Dict[str, Any]
    x_fapi_interaction_id: str


@dataclass
class TokenInput:
    access_token: str
    id_token: str
    token_type: str
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass
class MtlsEndpointAliases:
    token_endpoint: Optional[str] = None
    pushed_authorization_request_endpoint: Optional[str] = None
    authorization_endpoint: Optional[str] = None
    userinfo_endpoint: Optional[str] = None


@dataclass
class IssuerMetadata:
    issuer: str
    jwks_uri: str
    id_token_signing_alg_values_supported: List[str]
    token_endpoint: str
    pushed_authorization_request_endpoint: str
    authorization_endpoint: str
    userinfo_endpoint: str
    mtls_endpoint_aliases: MtlsEndpointAliases

    def get_preferred_token_endpoint(self) -> str:
        return self.mtls_endpoint_aliases.token_endpoint \
            if self.mtls_endpoint_aliases and self.mtls_endpoint_aliases.token_endpoint \
            else self.token_endpoint

    def get_preferred_pushed_authorization_request_endpoint(self) -> str:
        return self.mtls_endpoint_aliases.pushed_authorization_request_endpoint \
            if self.mtls_endpoint_aliases and self.mtls_endpoint_aliases.pushed_authorization_request_endpoint \
            else self.pushed_authorization_request_endpoint

    def get_preferred_authorization_endpoint(self) -> str:
        return self.mtls_endpoint_aliases.authorization_endpoint \
            if self.mtls_endpoint_aliases and self.mtls_endpoint_aliases.authorization_endpoint \
            else self.authorization_endpoint

    def get_preferred_userinfo_endpoint(self) -> str:
        return self.mtls_endpoint_aliases.userinfo_endpoint \
            if self.mtls_endpoint_aliases and self.mtls_endpoint_aliases.userinfo_endpoint \
            else self.userinfo_endpoint
