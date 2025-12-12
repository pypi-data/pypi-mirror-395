import contextvars
from contextlib import contextmanager
from typing import Any, Optional

from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import ChainedTokenCredential, EnvironmentCredential
from azure.identity._exceptions import CredentialUnavailableError
from fabric.analytics.environment.base.credentials import (
    IFabricAnalyticsTokenCredentialProviderPlugin,
)
from fabric.analytics.environment.context import FabricContext
from fabric.analytics.environment.plugin_provider import (
    BaseProvider,
    NoAvailableProvider,
)


class FabricAnalyticsTokenCredentials(TokenCredential):
    """
    Get Fabric Token Credential,
    **Priority:**
    **Values set via SetFabricAnalyticsDefaultTokenCredentials > Runtime default credential provided by plugin you installed**

    In below code:
    ```
    with SetFabricAnalyticsDefaultTokenCredentials(credential=MyCustomCredentialA()):

        FabricAnalyticsTokenCredentials() ## MyCustomCredentialA is used

        with SetFabricAnalyticsDefaultTokenCredentials(credential=MyCustomCredentialC()):
            FabricAnalyticsTokenCredentials() ## MyCustomCredentialC is used

        FabricAnalyticsTokenCredentials() ## MyCustomCredentialA is used

    FabricAnalyticsTokenCredentials() ## Plugin provides default credential, throw failure is no plugin is registered
    ```
    """

    def __init__(self, **kwargs):
        is_ppe = kwargs.pop("is_ppe", None)
        if is_ppe is None:
            is_ppe = FabricContext().internal_context.is_ppe()
        self.is_ppe = is_ppe
        self.use_ml_1p = kwargs.pop("use_ml_1p", True)

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        enable_cae: bool = False,
        **kwargs: Any,
    ) -> AccessToken:
        kwargs.setdefault("is_ppe", self.is_ppe)
        kwargs.setdefault("use_ml_1p", self.use_ml_1p)
        return FabricAnalyticsTokenCredentialProvider().get_token(
            *scopes, claims=claims, tenant_id=tenant_id, enable_cae=enable_cae, **kwargs
        )


context_credential = contextvars.ContextVar("context_credential", default=None)
gloabl_credential = None


@contextmanager
def SetFabricAnalyticsDefaultTokenCredentials(credential: TokenCredential):
    """
    with SetFabricAnalyticsDefaultTokenCredentials(InteractiveBrowserCredential(client_id="you-app-id")):
        <body1>
    <body2>
    body1 will use InteractiveBrowserCredential
    body2 will use any default credential previously

    Args:
        credential (TokenCredential): A credential you want to use within context
    """
    previous_credential = context_credential.get()
    context_credential.set(credential)
    try:
        yield
    finally:
        context_credential.set(previous_credential)


def SetFabricAnalyticsDefaultTokenCredentialsGlobally(credential: TokenCredential):
    global gloabl_credential
    gloabl_credential = credential


def ClearFabricAnalyticsDefaultTokenCredentialsGlobally():
    """Clear any override credential set by SetFabricAnalyticsDefaultTokenCredentialsGlobally globally"""
    global gloabl_credential
    gloabl_credential = None


class FabricAnalyticsTokenCredentialProvider(
    BaseProvider[IFabricAnalyticsTokenCredentialProviderPlugin]
):
    """
    Provide Fabric Credential by selecting appropriate credential provider plugins.
    Custom provider selection and initialization are both lazy.
    If you want initialization happen immediately, call load().

    We are not directly extending TokenCredential to avoid metaclass conflict,
    And TokenCredential is runtime checkable
    """

    plugin_entry_point_name = "fabric_analytics.token_credential_provider"

    def __init__(self):
        BaseProvider.__init__(self)
        self._register_entrypoints()

    @property
    def provider_plugin(self) -> TokenCredential:
        try:
            if context_credential.get() is not None:
                return context_credential.get()
            if gloabl_credential is not None:
                return gloabl_credential
            return super().provider_plugin
        except NoAvailableProvider as e:
            raise CredentialUnavailableError(str(e))

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        enable_cae: bool = False,
        **kwargs: Any,
    ) -> AccessToken:
        if self.provider_plugin == context_credential.get():
            kwargs.pop(
                "is_ppe"
            )  # This is plugin specific param, avoid pass to credential of any type
            kwargs.pop("use_ml_1p")
        return self.provider_plugin.get_token(
            *scopes, claims=claims, tenant_id=tenant_id, enable_cae=enable_cae, **kwargs
        )
