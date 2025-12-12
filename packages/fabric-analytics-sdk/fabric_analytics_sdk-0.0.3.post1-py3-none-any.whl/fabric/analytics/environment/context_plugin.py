import logging
from functools import lru_cache
from typing import Optional

from azure.core.pipeline.policies import HttpLoggingPolicy
from fabric.analytics.environment.utils.docstring import inherit_docs
from fabric.analytics.rest.fabric_client import FabricRestClient

from .base.context import ArtifactContext, IContextProvider, InternalContext
from .plugin_provider import IPlugin

# https://dev.azure.com/powerbi/Trident/_wiki/wikis/Trident.wiki/46148/Environments
SUPPORTED_FABRIC_REST_ENVIRONMENTS = {
    "onebox": "onebox-redirect.analysis.windows-int.net/",
    "daily": "dailyapi.fabric.microsoft.com/",
    "edog": "powerbiapi.analysis-df.windows.net/",
    "int3": "powerbiapi.analysis-df.windows.net/",
    "dxt": "dxtapi.fabric.microsoft.com/",
    "msit": "msitapi.fabric.microsoft.com/",
    "msitbcdr": "msitapi.fabric.microsoft.com/",
    "prod": "api.fabric.microsoft.com/",
}

SUPPORTED_ONELAKE_REST_ENVIRONMENTS = {
    "onebox": "localhost-onebox.pbidedicated.windows-int.net:10443/",
    "daily": "daily-onelake.dfs.fabric.microsoft.com/",
    "edog": "onelake-int-edog.pbidedicated.windows-int.net/",
    "int3": "onelake-int-edog.pbidedicated.windows-int.net/",
    "dxt": "dxt-onelake.dfs.fabric.microsoft.com/",
    "msit": "msit-onelake.dfs.fabric.microsoft.com/",
    "msitbcdr": "msit-onelake.dfs.fabric.microsoft.com/",
    "prod": "onelake.dfs.fabric.microsoft.com/",
}

logger = logging.getLogger(__name__)


@inherit_docs
class BaseContextProvider(IContextProvider):
    """This is base"""

    _runtime_name = "unknown"
    _workspace_id: Optional[str] = None

    @property
    def workspace_id(self) -> str:
        if BaseContextProvider._workspace_id is None:
            print(
                "Runtime plugin is not installed and default workspace_id is not set, please enter your workspace_id..."
            )
            BaseContextProvider._workspace_id = input(
                "Please enter the default workspace ID: "
            )
        return BaseContextProvider._workspace_id

    @property
    def runtime_name(self) -> str:
        """
        Return unique identifier of runtime environment
        """
        return self._runtime_name

    @property
    def artifact_context(self) -> Optional[ArtifactContext]:
        """
        Info of the notebook/sjd in execution.
        If it is not running in notebook/sjd, will be None
        """
        return None

    @property
    def internal_context(self) -> InternalContext:
        """
        Additional Internal Context
        """
        return InternalContext()

    @property
    def capacity_id(self) -> Optional[str]:
        """
        The id of capacity you operate on.
        """
        return _resolve_capacity_id(
            self.pbi_shared_host, self.internal_context.is_ppe(), self.workspace_id
        )

    @property
    def onelake_endpoint(self) -> str:
        """
        The URL of the Onelake endpoint, start with https://
        """
        if self.internal_context.is_wspl_enabled:
            return self._get_wspl_onelake_endpoint()

        return "https://" + SUPPORTED_ONELAKE_REST_ENVIRONMENTS.get(
            self.internal_context.rollout_stage, "onelake.dfs.fabric.microsoft.com/"
        )

    @property
    def pbi_shared_host(self) -> str:
        """
        The URL of the PowerBI shared host, start with https://
        e.g: https://api.fabric.microsoft.com
        """
        if self.internal_context.is_wspl_enabled and not self.internal_context.is_ppe():
            return self._get_wspl_shared_host()

        return "https://" + SUPPORTED_FABRIC_REST_ENVIRONMENTS.get(
            self.internal_context.rollout_stage, "api.fabric.microsoft.com/"
        )

    @property
    def pbi_cluster_host(self) -> str:
        """
        The URL of the PowerBI private host, start with https://
        e.g: https://DF-MSIT-SCUS-redirect.analysis.windows.net
        """
        if self.internal_context.is_wspl_enabled and not self.internal_context.is_ppe():
            return self._get_wspl_shared_host()

        return _resolve_pbi_cluster_host(
            self.pbi_shared_host, self.internal_context.is_ppe(), self.workspace_id
        )

    @property
    def mwc_workload_host(self) -> Optional[str]:
        """
        The URL of the MWC workload host, start with https://
        This is optional since connect to private api (mwc workload) is not a must
        """
        if self.internal_context.is_wspl_enabled:
            return self._get_wspl_mwc_workload_host()

        return _resolve_mwc_workload_host(
            self.pbi_cluster_host,
            self.internal_context.is_ppe(),
            self.capacity_id,
            self.workspace_id,
        )

    def _get_wspl_onelake_endpoint(self) -> str:
        """Get onelake endpoint wspl version"""
        if self.workspace_id is None:
            return None
        ws_id = self.workspace_id.lower().replace("-", "")
        pbienv = self.internal_context.rollout_stage
        env_mark = f"{pbienv}-" if pbienv in ["daily", "dxt", "msit"] else ""
        host = f"https://{ws_id}.z{ws_id[:2]}.{env_mark}onelake.fabric.microsoft.com/"
        return host

    def _get_wspl_mwc_workload_host(self) -> str:
        """Get onelake endpoint wspl version"""
        if self.workspace_id is None:
            return None
        ws_id = self.workspace_id.lower().replace("-", "")
        pbienv = self.internal_context.rollout_stage
        env_mark = f"{pbienv}-" if pbienv in ["daily", "dxt", "msit"] else ""
        host = f"https://{ws_id}.z{ws_id[:2]}.{env_mark}c.fabric.microsoft.com/"
        return host

    def _get_wspl_shared_host(self) -> str:
        """Get onelake endpoint wspl version"""
        if self.workspace_id is None:
            return None
        ws_id = self.workspace_id.lower().replace("-", "")
        pbienv = self.internal_context.rollout_stage
        env_mark = pbienv if pbienv in ["daily", "dxt", "msit"] else ""
        host = f"https://{ws_id}.z{ws_id[:2]}.w.{env_mark}api.fabric.microsoft.com/"
        return host


@lru_cache(maxsize=None)
def _resolve_capacity_id(pbi_shared_host: str, is_ppe: bool, workspace_id: str) -> str:
    client = FabricRestClient(endpoint=pbi_shared_host, is_ppe=is_ppe)
    resp = client.get(f"v1/workspaces/{workspace_id}")
    resp.raise_for_status()
    capacity_id = resp.json().get("capacityId")
    if not capacity_id:
        raise Exception(
            f"The workspcae {workspace_id}'s license doesn't support Fabric capabilities"
        )
    return capacity_id


@lru_cache(maxsize=None)
def _resolve_pbi_cluster_host(pbi_shared_host: str, is_ppe: bool, workspace_id: str):
    """The cache depends on workspace id"""
    client = FabricRestClient(
        endpoint=pbi_shared_host,
        is_ppe=is_ppe,
        http_logging_policy=HttpLoggingPolicy(),
    )
    resp = client.get("powerbi/globalservice/v201606/clusterDetails")
    resp.raise_for_status()
    return resp.json()["clusterUrl"]


@lru_cache(maxsize=None)
def _resolve_mwc_workload_host(
    pbi_cluster_host: str, is_ppe: bool, capacity_id: str, workspace_id: str
) -> str:
    try:
        client = FabricRestClient(
            endpoint=pbi_cluster_host,
            is_ppe=is_ppe,
            http_logging_policy=HttpLoggingPolicy(),
        )
        resp = client.post(
            "/metadata/v201606/generatemwctokenv2",
            json={
                "capacityObjectId": capacity_id,
                "workspaceObjectId": workspace_id,
                "workloadType": "ML",
            },
        )
        resp.raise_for_status()
        return "https://" + resp.json()["TargetUriHost"] + "/"
    except:
        logger.warning(
            "Unable to resolve mwc_workload_host, you may need to set it explicitly"
        )
        return ""


@inherit_docs
class BaseContextProviderPlugin(BaseContextProvider, IPlugin):
    @classmethod
    def in_context(cls):
        return False


class DefaultContextProviderPlugin(BaseContextProviderPlugin):
    priority: int = 255  # priority of default

    @classmethod
    def in_context(cls):
        return True
