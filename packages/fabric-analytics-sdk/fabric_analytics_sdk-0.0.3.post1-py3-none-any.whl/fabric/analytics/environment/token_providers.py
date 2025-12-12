import re

from azure.core.pipeline import PipelineContext, PipelineRequest
from azure.core.pipeline.policies import BearerTokenCredentialPolicy
from azure.core.pipeline.transport import HttpRequest
from fabric.analytics.environment.base.policies import MWCTokenCredentialPolicy
from fabric.analytics.environment.constant import PBI_SCOPE, PBI_SCOPE_PPE
from fabric.analytics.environment.context import FabricContext
from fabric.analytics.environment.credentials import FabricAnalyticsTokenCredentials
from fabric.analytics.environment.mwc_credential import (
    IFabricAnalyticsMWCCredential,
    MWCTokenCredentialV1,
    MWCTokenCredentialV2,
    MWCTokenRequestPayloadV1,
    MWCTokenRequestPayloadV2,
)


def _extract_bearer_token(header):
    # Regex to match "Bearer <token>"
    match = re.match(r"^Bearer (\S+)$", header)
    if match:
        return match.group(1)  # Returns the token
    else:
        return None  # Return None if the header format is incorrect


def _extract_mwc_token(header):
    # Regex to match "Bearer <token>"
    match = re.match(r"^mwctoken (\S+)$", header)
    if match:
        return match.group(1)  # Returns the token
    else:
        return None  # Return None if the header format is incorrect


class FabricAADTokenProvider:
    def __init__(self, *scopes: str, **kwargs):
        """
        The FabricAnalyticsTokenCredentials follows microsoft credential convention and don't have cache implementation.
        While we ususally uses other http client which need token directly, not the credential,
        This class serve the token while taking care of cache.
        """
        is_ppe = kwargs.pop("is_ppe", None)
        if is_ppe is None:
            is_ppe = FabricContext().internal_context.is_ppe()
        kwargs.setdefault("is_ppe", is_ppe)

        credential = FabricAnalyticsTokenCredentials(**kwargs)
        if len(scopes) == 0:
            self.scopes = (PBI_SCOPE_PPE,) if is_ppe else (PBI_SCOPE,)

        self.bearer_credential_policy = BearerTokenCredentialPolicy(
            credential, *self.scopes
        )

    def get_token(self) -> str:
        http_request = HttpRequest("GET", "https://example.org")
        pipeline_request = PipelineRequest(
            http_request, PipelineContext(transport=None)
        )
        self.bearer_credential_policy.on_request(pipeline_request)
        return _extract_bearer_token(
            pipeline_request.http_request.headers["Authorization"]
        )

    def get_auth_header(self) -> str:
        http_request = HttpRequest("GET", "https://example.org")
        pipeline_request = PipelineRequest(
            http_request, PipelineContext(transport=None)
        )
        self.bearer_credential_policy.on_request(pipeline_request)
        return pipeline_request.http_request.headers["Authorization"]


class FabricMWCTokenProvider:
    mwc_credential_policy: IFabricAnalyticsMWCCredential

    def get_token(self) -> str:
        http_request = HttpRequest("GET", "https://example.org")
        pipeline_request = PipelineRequest(
            http_request, PipelineContext(transport=None)
        )
        self.mwc_credential_policy.on_request(pipeline_request)
        return _extract_mwc_token(
            pipeline_request.http_request.headers["Authorization"]
        )

    def get_auth_header(self) -> str:
        http_request = HttpRequest("GET", "https://example.org")
        pipeline_request = PipelineRequest(
            http_request, PipelineContext(transport=None)
        )
        self.mwc_credential_policy.on_request(pipeline_request)
        return pipeline_request.http_request.headers["Authorization"]


class FabricMWCTokenV1Provider(FabricMWCTokenProvider):
    def __init__(self, payload: MWCTokenRequestPayloadV1):
        """
        We ususally uses other http client which need token directly, not the credential,
        This class serve the token while taking care of cache.
        """
        credential = MWCTokenCredentialV1(payload)

        self.mwc_credential_policy = MWCTokenCredentialPolicy(credential)


class FabricMWCTokenV2Provider(FabricMWCTokenProvider):
    def __init__(self, payload: MWCTokenRequestPayloadV2):
        """
        We ususally uses other http client which need token directly, not the credential,
        This class serve the token while taking care of cache.
        """
        credential = MWCTokenCredentialV2(payload)

        self.mwc_credential_policy = MWCTokenCredentialPolicy(credential)
