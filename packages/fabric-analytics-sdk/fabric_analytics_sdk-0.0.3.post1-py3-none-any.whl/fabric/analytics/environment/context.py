import contextvars
import copy
import logging
import threading
from collections import namedtuple
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Optional, cast

from fabric.analytics.environment.base.context import (
    ArtifactContext,
    IContextProvider,
    IContextProviderPlugin,
    InternalContext,
)
from fabric.analytics.environment.plugin_provider import (
    BaseProvider,
    NoAvailableProvider,
)
from fabric.analytics.environment.utils.docstring import inherit_docs

logger = logging.getLogger(__name__)


_UNSET = "_UNSET"  # When you pass this, setting will be ignored, while passing None will overwrite value to None


class FabricContext(IContextProvider):
    """
    Initialize Fabric Context,
    **Priority:**
    **Value explicitly passed > Values set via SetFabricDefaultContext > Runtime default values provided by plugin you installed**

    with SetFabricDefaultContext(workspace_id='aaa'):

        FabricContext(workspace_id='bbb').workspace_id  ## bbb
        FabricContext().workspace_id                    ## aaa

        with SetFabricDefaultContext(workspace_id='ccc'):
            FabricContext().workspace_id                ## ccc

        FabricContext().workspace_id                    ## aaa

    FabricContext().workspace_id ## Plugin provides default context, throw failure is no plugin is registered

    !!! cloudpickle only Serialize static values you set via __init__, it won't consider your plugin or `SetFabricDefaultContextGlobally` provided values.
    """

    def __init__(
        self,
        capacity_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        onelake_endpoint: Optional[str] = None,
        pbi_shared_host: Optional[str] = None,
        pbi_cluster_host: Optional[str] = None,
        mwc_workload_host: Optional[str] = None,
        artifact_context: Optional[ArtifactContext] = None,
        internal_context: Optional[InternalContext] = None,
    ):
        self._context_provider = ContextProvider()
        self._static_context = StaticFabricContext(
            capacity_id=capacity_id,
            workspace_id=workspace_id,
            onelake_endpoint=onelake_endpoint,
            pbi_shared_host=pbi_shared_host,
            pbi_cluster_host=pbi_cluster_host,
            mwc_workload_host=mwc_workload_host,
            artifact_context=artifact_context,
            internal_context=internal_context,
        )
        super().__init__()

    def to_dict(self) -> Dict[str, Any]:
        """Convert an object into a named tuple, including only properties."""

        # Get all attributes, including @property methods
        attributes = {
            attr: str(getattr(self, attr))
            for attr in dir(self)
            if not attr.startswith("__")  # Ignore dunder methods
            and not callable(getattr(self, attr, None))  # Ignore methods
            and isinstance(getattr(type(self), attr, None), property)
        }

        return attributes

    def __str__(self):
        return f"{self.to_dict()}"

    @property
    def runtime_name(self) -> str:
        try:
            return self._context_provider.provider_plugin.runtime_name.fget(self)
        except NoAvailableProvider:
            return "unknown"

    @property
    def capacity_id(self) -> Optional[str]:
        if self._static_context.capacity_id:
            return self._static_context.capacity_id
        if fabric_default_context_override.capacity_id is not None:
            return fabric_default_context_override.capacity_id
        return type(self._context_provider.provider_plugin).capacity_id.fget(self)

    @capacity_id.setter
    def capacity_id(self, value: Optional[str]) -> None:
        self._static_context.capacity_id = value

    @property
    def workspace_id(self) -> Optional[str]:
        if self._static_context.workspace_id:
            return self._static_context.workspace_id
        if fabric_default_context_override.workspace_id is not None:
            return fabric_default_context_override.workspace_id
        return type(self._context_provider.provider_plugin).workspace_id.fget(self)

    @workspace_id.setter
    def workspace_id(self, value: Optional[str]) -> None:
        self._static_context.workspace_id = value

    @property
    def onelake_endpoint(self) -> Optional[str]:
        if self._static_context.onelake_endpoint:
            return self._static_context.onelake_endpoint
        if fabric_default_context_override.onelake_endpoint is not None:
            return fabric_default_context_override.onelake_endpoint
        return type(self._context_provider.provider_plugin).onelake_endpoint.fget(self)

    @onelake_endpoint.setter
    def onelake_endpoint(self, value: Optional[str]) -> None:
        self._static_context.onelake_endpoint = value

    @property
    def pbi_shared_host(self) -> Optional[str]:
        if self._static_context.pbi_shared_host:
            return self._static_context.pbi_shared_host
        if fabric_default_context_override.pbi_shared_host is not None:
            return fabric_default_context_override.pbi_shared_host
        return type(self._context_provider.provider_plugin).pbi_shared_host.fget(self)

    @pbi_shared_host.setter
    def pbi_shared_host(self, value: Optional[str]) -> None:
        self._static_context.pbi_shared_host = value

    @property
    def pbi_cluster_host(self) -> Optional[str]:
        if self._static_context.pbi_cluster_host:
            return self._static_context.pbi_cluster_host
        if fabric_default_context_override.pbi_cluster_host is not None:
            return fabric_default_context_override.pbi_cluster_host
        return type(self._context_provider.provider_plugin).pbi_cluster_host.fget(self)

    @pbi_cluster_host.setter
    def pbi_cluster_host(self, value: Optional[str]) -> None:
        self._static_context.pbi_cluster_host = value

    @property
    def mwc_workload_host(self) -> Optional[str]:
        if self._static_context.mwc_workload_host:
            return self._static_context.mwc_workload_host
        if fabric_default_context_override.mwc_workload_host is not None:
            return fabric_default_context_override.mwc_workload_host
        return type(self._context_provider.provider_plugin).mwc_workload_host.fget(self)

    @mwc_workload_host.setter
    def mwc_workload_host(self, value: Optional[str]) -> None:
        self._static_context.mwc_workload_host = value

    @property
    def artifact_context(self) -> ArtifactContext:
        if self._static_context.artifact_context:
            return self._static_context.artifact_context
        if fabric_default_context_override.artifact_context is not None:
            return fabric_default_context_override.artifact_context
        return type(self._context_provider.provider_plugin).artifact_context.fget(self)

    @artifact_context.setter
    def artifact_context(self, value: ArtifactContext) -> None:
        self._static_context.artifact_context = value

    @property
    def internal_context(self) -> InternalContext:
        if self._static_context.internal_context:
            return self._static_context.internal_context
        if fabric_default_context_override.internal_context is not None:
            return fabric_default_context_override.internal_context
        return type(self._context_provider.provider_plugin).internal_context.fget(self)

    @internal_context.setter
    def internal_context(self, value: InternalContext) -> None:
        self._static_context.internal_context = value

    # Fallback delegation
    def __getattr__(self, name):
        attr = getattr(self._context_provider.provider_plugin, name)
        if callable(attr):
            # Rebind 'self' so that 'self' inside A.method_* refers to this B instance
            def wrapper(*args, **kwargs):
                return attr.__func__(self, *args, **kwargs)

            return wrapper
        return attr

    def __getstate__(self):
        return {"_static_context": self._static_context}

    def __setstate__(self, state):
        # Restore the object from the state; reinitialize _secret if needed
        self._static_context = state["_static_context"]
        self._context_provider = ContextProvider()


@inherit_docs
class ContextProvider(BaseProvider[IContextProviderPlugin]):
    """
    Provide Fabric Context by selecting appropriate context provider plugins.
    Custom provider selection and initialization are both lazy.
    If you want initialization happen immediately, call load().
    """

    plugin_entry_point_name = "fabric_analytics.context_provider"

    def __init__(self):
        BaseProvider.__init__(self)

    @property
    def provider_plugin(self) -> IContextProviderPlugin:
        return super().provider_plugin


class StaticFabricContext:
    def __init__(
        self,
        capacity_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        onelake_endpoint: Optional[str] = None,
        pbi_shared_host: Optional[str] = None,
        pbi_cluster_host: Optional[str] = None,
        mwc_workload_host: Optional[str] = None,
        artifact_context: Optional["ArtifactContext"] = None,
        internal_context: Optional["InternalContext"] = None,
    ):
        self.capacity_id = capacity_id
        self.workspace_id = workspace_id
        self.onelake_endpoint = onelake_endpoint
        self.pbi_shared_host = pbi_shared_host
        self.pbi_cluster_host = pbi_cluster_host
        self.mwc_workload_host = mwc_workload_host
        self.artifact_context = artifact_context
        self.internal_context = internal_context

    # --- setters with _UNSET support ---
    def set_capacity_id(self, value=_UNSET):
        if value is not _UNSET:
            self.capacity_id = value

    def set_workspace_id(self, value=_UNSET):
        if value is not _UNSET:
            self.workspace_id = value

    def set_onelake_endpoint(self, value=_UNSET):
        if value is not _UNSET:
            self.onelake_endpoint = value

    def set_pbi_shared_host(self, value=_UNSET):
        if value is not _UNSET:
            self.pbi_shared_host = value

    def set_pbi_cluster_host(self, value=_UNSET):
        if value is not _UNSET:
            self.pbi_cluster_host = value

    def set_mwc_workload_host(self, value=_UNSET):
        if value is not _UNSET:
            self.mwc_workload_host = value

    def set_artifact_context(self, value=_UNSET):
        if value is not _UNSET:
            self.artifact_context = value

    def set_internal_context(self, value=_UNSET):
        if value is not _UNSET:
            self.internal_context = value


class FabricContextOverride:
    def __init__(self):
        self.context_local: ContextVar["StaticFabricContext"] = contextvars.ContextVar(
            "fabric_default_context_override", default=StaticFabricContext()
        )
        self.context_global: StaticFabricContext = StaticFabricContext()

    @property
    def workspace_id(self) -> Optional[str]:
        return self.context_local.get().workspace_id or self.context_global.workspace_id

    @property
    def capacity_id(self) -> Optional[str]:
        return self.context_local.get().capacity_id or self.context_global.capacity_id

    @property
    def onelake_endpoint(self) -> Optional[str]:
        return (
            self.context_local.get().onelake_endpoint
            or self.context_global.onelake_endpoint
        )

    @property
    def pbi_shared_host(self) -> Optional[str]:
        return (
            self.context_local.get().pbi_shared_host
            or self.context_global.pbi_shared_host
        )

    @property
    def pbi_cluster_host(self) -> Optional[str]:
        return (
            self.context_local.get().pbi_cluster_host
            or self.context_global.pbi_cluster_host
        )

    @property
    def mwc_workload_host(self) -> Optional[str]:
        return (
            self.context_local.get().mwc_workload_host
            or self.context_global.mwc_workload_host
        )

    @property
    def artifact_context(self) -> Optional[str]:
        return (
            self.context_local.get().artifact_context
            or self.context_global.artifact_context
        )

    @property
    def internal_context(self) -> Optional[str]:
        return (
            self.context_local.get().internal_context
            or self.context_global.internal_context
        )


# This is overrideable
fabric_default_context_override = FabricContextOverride()


@contextmanager
def SetFabricDefaultContext(
    capacity_id: Optional[str] = _UNSET,
    workspace_id: Optional[str] = _UNSET,
    onelake_endpoint: Optional[str] = _UNSET,
    pbi_shared_host: Optional[str] = _UNSET,
    pbi_cluster_host: Optional[str] = _UNSET,
    mwc_workload_host: Optional[str] = _UNSET,
    artifact_context: Optional[ArtifactContext] = _UNSET,
    internal_context: Optional[InternalContext] = _UNSET,
):
    """
    This override context-local default fabirc context returned by DefaultFabricContext()
    with SetFabricDefaultContext(workspace_id="xxx"):
        <body1>
    <body2>
    body1 will see new workspace_id
    body2 will see previous default workspace_id
    """
    ctx_local = fabric_default_context_override.context_local.get()

    # Save old values
    prev = StaticFabricContext(
        capacity_id=ctx_local.capacity_id,
        workspace_id=ctx_local.workspace_id,
        onelake_endpoint=ctx_local.onelake_endpoint,
        pbi_shared_host=ctx_local.pbi_shared_host,
        pbi_cluster_host=ctx_local.pbi_cluster_host,
        mwc_workload_host=ctx_local.mwc_workload_host,
        artifact_context=ctx_local.artifact_context,
        internal_context=ctx_local.internal_context,
    )
    try:
        # Apply only values that are not _UNSET
        ctx_local.set_capacity_id(capacity_id)
        ctx_local.set_workspace_id(workspace_id)
        ctx_local.set_onelake_endpoint(onelake_endpoint)
        ctx_local.set_pbi_shared_host(pbi_shared_host)
        ctx_local.set_pbi_cluster_host(pbi_cluster_host)
        ctx_local.set_mwc_workload_host(mwc_workload_host)
        ctx_local.set_artifact_context(artifact_context)
        ctx_local.set_internal_context(internal_context)

        yield  # run the body inside the override

    finally:
        # Restore previous global context
        ctx_local.set_capacity_id(prev.capacity_id)
        ctx_local.set_workspace_id(prev.workspace_id)
        ctx_local.set_onelake_endpoint(prev.onelake_endpoint)
        ctx_local.set_pbi_shared_host(prev.pbi_shared_host)
        ctx_local.set_pbi_cluster_host(prev.pbi_cluster_host)
        ctx_local.set_mwc_workload_host(prev.mwc_workload_host)
        ctx_local.set_artifact_context(prev.artifact_context)
        ctx_local.set_internal_context(prev.internal_context)


@contextmanager
def SetFabricDefaultContextGlobally(
    capacity_id: Optional[str] = _UNSET,
    workspace_id: Optional[str] = _UNSET,
    onelake_endpoint: Optional[str] = _UNSET,
    pbi_shared_host: Optional[str] = _UNSET,
    pbi_cluster_host: Optional[str] = _UNSET,
    mwc_workload_host: Optional[str] = _UNSET,
    artifact_context: Optional[ArtifactContext] = _UNSET,
    internal_context: Optional[InternalContext] = _UNSET,
):
    """
    This override context-local default fabirc context returned by DefaultFabricContext()
    with SetFabricDefaultContext(workspace_id="xxx"):
        <body1>
    <body2>
    body1 will see new workspace_id
    body2 will see previous default workspace_id
    """
    ctx_global = fabric_default_context_override.context_global
    ctx_global.set_capacity_id(capacity_id)
    ctx_global.set_workspace_id(workspace_id)
    ctx_global.set_onelake_endpoint(onelake_endpoint)
    ctx_global.set_pbi_shared_host(pbi_shared_host)
    ctx_global.set_pbi_cluster_host(pbi_cluster_host)
    ctx_global.set_mwc_workload_host(mwc_workload_host)
    ctx_global.set_artifact_context(artifact_context)
    ctx_global.set_internal_context(internal_context)


def ClearFabricDefaultContextGlobally():
    """Clear any override context set by SetFabricDefaultContextGlobal"""
    fabric_default_context_override.context_global = StaticFabricContext()
