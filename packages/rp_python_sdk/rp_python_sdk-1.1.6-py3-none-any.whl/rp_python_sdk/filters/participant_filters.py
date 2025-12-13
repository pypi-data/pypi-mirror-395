from datetime import datetime, date
from typing import List

from rp_python_sdk.model import Participant
from rp_python_sdk.sdk_config import CertificationFilter


def remove_out_of_date_certifications(participants: List[Participant], reference_date: date) -> List[Participant]:
    for participant in participants:
        for auth_server in participant.authorisation_servers:
            filtered = [certification for certification in auth_server.authorisation_server_certifications if
                        to_date(certification.certification_start_date) < reference_date < to_date(
                            certification.certification_expiration_date)]
            auth_server.authorisation_server_certifications = filtered

    return participants


def remove_unofficial_certifications(participants: List[Participant]) -> List[Participant]:
    for participant in participants:
        for auth_server in participant.authorisation_servers:
            filtered = [certification for certification in auth_server.authorisation_server_certifications
                        if certification.status == "Certified"]

            auth_server.authorisation_server_certifications = filtered

    return participants


def remove_inactive_auth_servers(participants: List[Participant]) -> List[Participant]:
    for participant in participants:
        filtered = [auth_server for auth_server in participant.authorisation_servers if any(
            certification.profile_type == "Redirect" and certification.profile_variant == "FAPI2 Adv. OP w/Private Key, PAR"
            for certification in auth_server.authorisation_server_certifications)]

        participant.authorisation_servers = filtered

    return participants


def remove_participants_without_auth_servers(participants: List[Participant]) -> List[Participant]:
    return [participant for participant in participants if participant.authorisation_servers]


def filter_auth_servers_for_supported_claims(participants: List[Participant], claims: List[str]) -> List[Participant]:
    name_claims = ["name", "given_name", "middle_name", "family_name"]
    has_name_claims = any(claim in name_claims for claim in claims)

    formatted_claims = ["name"] + [claim for claim in claims if
                                   claim not in name_claims] if has_name_claims else claims

    for participant in participants:
        filtered = [auth_server for auth_server in participant.authorisation_servers
                    if set([certification.profile_variant for certification in
                            auth_server.authorisation_server_certifications
                            if certification.profile_type == "ConnectID Claims"]).issuperset(formatted_claims)]

        participant.authorisation_servers = filtered

    return participants


def filter_for_required_certifications(participants: List[Participant],
                                       certifications: List[CertificationFilter]) -> List[Participant]:
    for certification in certifications:
        for participant in participants:
            filtered = [auth_server for auth_server in participant.authorisation_servers if any(
                server_certification.profile_type == certification.profile_type and server_certification.profile_variant == certification.profile_variant
                for server_certification in auth_server.authorisation_server_certifications)]

            participant.authorisation_servers = filtered

    return participants


def remove_fallback_identity_service_provider(participants: List[Participant]) -> List[Participant]:
    for participant in participants:
        filtered = [auth_server for auth_server in participant.authorisation_servers if not any(
            certification.profile_type == "ConnectID" and certification.profile_variant == "Fallback Identity Service Provider"
            for certification in auth_server.authorisation_server_certifications)]
        participant.authorisation_servers = filtered

    return participants


def filter_for_fallback_identity_service_providers(participants: List[Participant]) -> List[Participant]:
    for participant in participants:
        filtered = [auth_server for auth_server in participant.authorisation_servers if any(
            certification.profile_type == "ConnectID" and certification.profile_variant == "Fallback Identity Service Provider"
            for certification in auth_server.authorisation_server_certifications)]

        participant.authorisation_servers = filtered

    return participants


def to_date(date_string: str) -> date:
    date_format = "%d/%m/%Y"
    return datetime.strptime(date_string, date_format).date()
