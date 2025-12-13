from rp_python_sdk.endpoints.util.system_info import get_system_info
from rp_python_sdk.endpoints.util.version_info import get_version_info


def build_user_agent(client_id: str) -> str:
    version = get_version_info()
    platform = get_system_info()
    return f"cid-rp-python-sdk/{version} ({platform}) +{client_id}"
