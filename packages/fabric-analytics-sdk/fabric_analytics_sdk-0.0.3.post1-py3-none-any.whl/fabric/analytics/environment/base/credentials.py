import base64
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from azure.core.credentials import AccessToken, TokenCredential
from fabric.analytics.environment.base.plugin import IPlugin

logger = logging.getLogger(__name__)


class MwcToken:
    def __init__(
        self, TargetUriHost: str = "", CapacityObjectId: str = "", Token: str = ""
    ):
        self.TargetUriHost = TargetUriHost
        self.CapacityObjectId = CapacityObjectId
        self.Token = Token


class MwcAccessToken(NamedTuple):
    """Represents an MWC token."""

    token: MwcToken
    """The token string."""
    expires_on: int
    """The token's expiration time in Unix time."""
    refresh_on: int

    @classmethod
    def build_from_json(cls, token_response):
        token = MwcToken(
            Token=token_response.get("Token"),
            CapacityObjectId=token_response.get("CapacityObjectId"),
            TargetUriHost=token_response.get("TargetUriHost"),
        )
        expires_on = _get_token_expire_time(token.Token)
        return MwcAccessToken(
            token=token, expires_on=expires_on, refresh_on=expires_on - 60
        )


class ArtifactTokenRequest(NamedTuple):
    artifactObjectId: str
    artifactType: str


class MWCTokenRequestPayloadV2:
    def __init__(
        self,
        workspace_id: str,
        workload_type: str = "ML",
        artifacts: List[ArtifactTokenRequest] = [],
    ):
        self.workspace_id: str = workspace_id
        self.workload_type: str = workload_type
        self.artifacts: List[ArtifactTokenRequest] = artifacts

    def to_dict(self):
        return {
            "workspaceObjectId": self.workspace_id,
            "workloadType": self.workload_type,
            "artifacts": [a._asdict() for a in self.artifacts],
        }

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)


class MWCTokenRequestPayloadV1:
    def __init__(
        self,
        capacity_id: str,
        workspace_id: str,
        workload_type: str = "ML",
        artifact_ids: List[str] = [],
    ):
        self.capacity_id = capacity_id
        self.workspace_id: str = workspace_id
        self.workload_type: str = workload_type
        self.artifact_ids: List[str] = artifact_ids

    def to_dict(self):
        return {
            "capacityObjectId": self.capacity_id,
            "workspaceObjectId": self.workspace_id,
            "workloadType": self.workload_type,
            "artifactObjectIds": self.artifact_ids,
        }

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)


class IFabricAnalyticsMWCCredential(ABC):
    @abstractmethod
    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        pass


class IFabricAnalyticsTokenCredentialProviderPlugin(IPlugin, TokenCredential):
    pass


class IFabricAnalyticsMWCCredentialProviderPlugin(
    IPlugin, IFabricAnalyticsMWCCredential
):
    pass


def _get_token_expire_time(token: str) -> int:
    # return expire timestamp in sec
    if not token:
        return 0
    try:
        payload = decode_jwt(token)
        if not payload:
            raise Exception("Invalid jwt token payload")
        exp_time = payload.get("exp", 0)
        return int(exp_time)
    except Exception:
        return 0


class FabricAnalyticsTokenCredentialProviderWithCacheMixin(
    IFabricAnalyticsTokenCredentialProviderPlugin
):
    def __init__(
        self, initial_tokens: Dict[str, str] = {}, threshold_time_to_refresh=60
    ):
        self._token_cache: Dict[str, AccessToken] = {}
        self.THRESHOLD_TIME_TO_REFRESH = threshold_time_to_refresh
        if initial_tokens:
            for resource in initial_tokens:
                self._token_cache[resource] = AccessToken(
                    initial_tokens[resource],
                    _get_token_expire_time(initial_tokens[resource]),
                )
        super().__init__()

    def _get_valid_token_from_cache(self, resource: str) -> AccessToken:
        cached_token = self._token_cache.get(resource)
        if self._check_token_valid(cached_token):
            return cached_token
        return None

    def get_access_token(self, resource: str) -> AccessToken:
        cached_token = self._get_valid_token_from_cache(resource)
        if not cached_token:
            new_token = self._get_access_token(resource)
            if new_token:
                self._token_cache[resource] = new_token
                return new_token
            else:
                raise Exception(f"get_access_token for {resource} returns empty result")
        else:
            return cached_token

    @abstractmethod
    def _get_access_token(self, resource: str) -> AccessToken:
        raise Exception("method not implemented")

    def _check_token_valid(self, token: AccessToken) -> Tuple[bool, int]:
        """
        Returns (is_valid, exp_time)
        """
        if not token or not token.token:
            return False, 0

        now = int(time.time())
        return now < token.expires_on - self.THRESHOLD_TIME_TO_REFRESH


def decode_base64url(base64url):
    """Decodes a Base64 URL encoded string."""
    # Replace URL-safe base64 characters with regular base64 characters
    padding = "=" * (4 - (len(base64url) % 4))  # Add padding if necessary
    base64url = base64url + padding
    base64_bytes = base64url.translate(str.maketrans("-_", "+/")).encode("utf-8")

    # Decode and return the result
    return base64.urlsafe_b64decode(base64_bytes)


def decode_jwt(token) -> Optional[Dict[str, Any]]:
    """Decodes the JWT token and returns the JSON payload."""
    try:
        # Split the JWT into its three components
        header_b64, payload_b64, signature_b64 = token.split(".")

        # Decode the payload (second part)
        decoded_payload = decode_base64url(payload_b64)

        # Convert the decoded payload to a dictionary (JSON)
        payload = json.loads(decoded_payload.decode("utf-8"))

        return payload
    except Exception as e:
        logger.exception(f"Error decoding JWT: {e}")
        return None
