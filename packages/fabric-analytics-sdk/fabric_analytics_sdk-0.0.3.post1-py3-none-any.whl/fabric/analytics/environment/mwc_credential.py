import contextvars
from contextlib import contextmanager
from typing import Any, Optional

from fabric.analytics.environment.base.credentials import (
    IFabricAnalyticsMWCCredential,
    IFabricAnalyticsMWCCredentialProviderPlugin,
    MwcAccessToken,
    MWCTokenRequestPayloadV1,
    MWCTokenRequestPayloadV2,
)
from fabric.analytics.environment.plugin_provider import BaseProvider
from fabric.analytics.rest.fabric_client import FabricRestClient

context_mwc_tokencredential_v1 = contextvars.ContextVar(
    "context_mwc_tokencredential_v1", default=None
)
global_context_mwc_tokencredential_v1: Optional[IFabricAnalyticsMWCCredential] = None


@contextmanager
def SetFabricAnalyticsDefaultMWCCredentialsV1(
    credential: IFabricAnalyticsMWCCredential,
):
    """
    with SetFabricAnalyticsDefaultMWCCredentialsV1(your_mwc_credential_v1):
        <body1>
    <body2>
    body1 will use your_mwc_credential_v2
    body2 will use any default credential previously

    Args:
        credential (IFabricAnalyticsMWCCredential): A mwc credential you want to use within context
    """
    previous_credential = context_mwc_tokencredential_v1.get()
    context_mwc_tokencredential_v1.set(credential)
    try:
        yield
    finally:
        context_mwc_tokencredential_v1.set(previous_credential)


def SetFabricAnalyticsDefaultMWCCredentialsGloballyV1(
    credential: IFabricAnalyticsMWCCredential,
):
    global global_context_mwc_tokencredential_v1
    global_context_mwc_tokencredential_v1 = credential


def ClearFabricAnalyticsDefaultMWCCredentialsGloballyV1():
    """Clear any override credential set by SetFabricAnalyticsDefaultMWCCredentialsGloballyV1 globally"""
    global global_context_mwc_tokencredential_v1
    global_context_mwc_tokencredential_v1 = None


context_mwc_tokencredential_v2 = contextvars.ContextVar(
    "context_mwc_tokencredential_v2", default=None
)
global_context_mwc_tokencredential_v2: Optional[IFabricAnalyticsMWCCredential] = None


@contextmanager
def SetFabricAnalyticsDefaultMWCCredentialsV2(
    credential: IFabricAnalyticsMWCCredential,
):
    """
    with SetFabricAnalyticsDefaultMWCCredentialsV2(your_mwc_credential_v2):
        <body1>
    <body2>
    body1 will use your_mwc_credential_v2
    body2 will use any default credential previously

    Args:
        credential (IFabricAnalyticsMWCCredential): A mwc credential you want to use within context
    """
    previous_credential = context_mwc_tokencredential_v2.get()
    context_mwc_tokencredential_v2.set(credential)
    try:
        yield
    finally:
        context_mwc_tokencredential_v2.set(previous_credential)


def SetFabricAnalyticsDefaultMWCCredentialsGloballyV2(
    credential: IFabricAnalyticsMWCCredential,
):
    global global_context_mwc_tokencredential_v2
    global_context_mwc_tokencredential_v2 = credential


def ClearFabricAnalyticsDefaultMWCCredentialsGloballyV2():
    """Clear any override credential set by SetFabricAnalyticsDefaultMWCCredentialsGloballyV2 globally"""
    global global_context_mwc_tokencredential_v2
    global_context_mwc_tokencredential_v2 = None


class MWCTokenCredentialV1(IFabricAnalyticsMWCCredential):
    def __init__(self, payload: MWCTokenRequestPayloadV1):
        BaseProvider.__init__(self)
        self.payload = payload

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        kwargs.setdefault("payload", self.payload)
        return _MWCTokenCredentialV1Provider().get_mwc_token(**kwargs)


class MWCTokenCredentialV2(IFabricAnalyticsMWCCredential):
    def __init__(self, payload: MWCTokenRequestPayloadV2):
        BaseProvider.__init__(self)
        self.payload = payload

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        kwargs.setdefault("payload", self.payload)
        return _MWCTokenCredentialV2Provider().get_mwc_token(**kwargs)


class _MWCTokenCredentialV1Provider(
    BaseProvider[IFabricAnalyticsMWCCredentialProviderPlugin]
):
    plugin_entry_point_name = "fabric_analytics.token_credential_provider_v1"

    def __init__(self):
        BaseProvider.__init__(self)
        self._register_entrypoints()

    @property
    def provider_plugin(self) -> IFabricAnalyticsMWCCredentialProviderPlugin:
        if context_mwc_tokencredential_v1.get() is not None:
            return context_mwc_tokencredential_v1.get()
        if global_context_mwc_tokencredential_v1 is not None:
            return global_context_mwc_tokencredential_v1
        return super().provider_plugin

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        return self.provider_plugin.get_mwc_token(**kwargs)


class _MWCTokenCredentialV2Provider(
    BaseProvider[IFabricAnalyticsMWCCredentialProviderPlugin]
):
    plugin_entry_point_name = "fabric_analytics.token_credential_provider_v2"

    def __init__(self):
        BaseProvider.__init__(self)
        self._register_entrypoints()

    @property
    def provider_plugin(self) -> IFabricAnalyticsMWCCredentialProviderPlugin:
        if context_mwc_tokencredential_v2.get() is not None:
            return context_mwc_tokencredential_v2.get()
        if global_context_mwc_tokencredential_v2 is not None:
            return global_context_mwc_tokencredential_v2
        return super().provider_plugin

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        return self.provider_plugin.get_mwc_token(**kwargs)


class BaseMWCTokenCredentialProviderV1(IFabricAnalyticsMWCCredentialProviderPlugin):
    priority: int = 255  # priority of default

    def __init__(
        self,
        payload: Optional[MWCTokenRequestPayloadV1] = None,
    ):
        self.payload = payload
        super().__init__()

    @classmethod
    def in_context(cls):
        return True

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        payload = self.payload or kwargs.pop("payload")
        if not payload:
            raise RuntimeError("missing required payload to generate mwc token")
        client = FabricRestClient()
        resp = client.get("powerbi/globalservice/v201606/clusterDetails")
        resp.raise_for_status()

        cluster_url = resp.json()["clusterUrl"]

        resp = FabricRestClient(endpoint=cluster_url).post(
            "metadata/v201606/generatemwctoken",
            data=payload.to_json(),
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise Exception("failed refresh mwc token!")
        return MwcAccessToken.build_from_json(resp.json())


class BaseMWCTokenCredentialProviderV2(IFabricAnalyticsMWCCredentialProviderPlugin):
    priority: int = 255  # priority of default

    def __init__(
        self,
        payload: Optional[MWCTokenRequestPayloadV2] = None,
    ):
        self.payload = payload
        super().__init__()

    @classmethod
    def in_context(cls):
        return True

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        payload = self.payload or kwargs.pop("payload")
        if not payload:
            raise RuntimeError("missing required payload to generate mwc token")
        client = FabricRestClient()
        resp = client.get("powerbi/globalservice/v201606/clusterDetails")
        resp.raise_for_status()

        cluster_url = resp.json()["clusterUrl"]

        resp = FabricRestClient(endpoint=cluster_url).post(
            "metadata/v201606/generatemwctokenv2",
            data=payload.to_json(),
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise Exception("failed refresh mwc token!")
        return MwcAccessToken.build_from_json(resp.json())
