from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from fabric.analytics.environment.base.plugin import IPlugin
from fabric.analytics.environment.utils.docstring import inherit_docs

ARTIFACT_TYPE_NOTEBOOK = "SynapseNotebook"
ARTIFACT_TYPE_LAKEHOUSE = "Lakehouse"
ARTIFACT_TYPE_EXPERIMENT = "MLExperiment"
ARTIFACT_TYPE_REGISTERED_MODEL = "MLModel"
ARTIFACT_TYPE_SJD = "SparkJobDefinition"
ARTIFACT_TYPE_GENRIC = "Item"


class ArtifactContext:
    def __init__(
        self,
        artifact_id: str,  # Notebook/SJD id
        attached_lakehouse_id: Optional[str] = None,
        attached_lakehouse_workspace_id: Optional[str] = None,
        artifact_type: str = ARTIFACT_TYPE_NOTEBOOK,
        session_id: Optional[str] = None,  # Running Livy ID in Fabric Notebook/SJD
    ):
        self.artifact_id = artifact_id
        self.attached_lakehouse_id = attached_lakehouse_id
        self.attached_lakehouse_workspace_id = attached_lakehouse_workspace_id
        self.artifact_type = artifact_type
        self.session_id = session_id

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"{self.to_dict()}"


class InternalContext:
    def __init__(
        self,
        rollout_stage: str = "prod",
        region: Optional[str] = None,
        is_wspl_enabled: bool = False,
    ):
        self.rollout_stage = rollout_stage.lower()
        self.region = region.lower() if region else None
        self.is_wspl_enabled = is_wspl_enabled

    def is_ppe(self) -> bool:
        return self.rollout_stage in ["cst", "edog", "int3", "onebox"]

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"{self.to_dict()}"


class IContextProvider(ABC):
    @property
    @abstractmethod
    def workspace_id(self) -> Optional[str]:
        """
        The id of workspace you operate on.
        """
        pass

    @property
    @abstractmethod
    def runtime_name(self) -> str:
        """
        Return unique identifier of runtime environment
        """
        pass

    @property
    @abstractmethod
    def internal_context(self) -> InternalContext:
        """
        Additional Internal Context
        """
        pass

    @property
    @abstractmethod
    def pbi_shared_host(self) -> str:
        """
        The Scheme+Host of PowerBI shared host, start with https://
        e.g: https://DF-MSIT-SCUS-redirect.analysis.windows.net
        Which is the endpoint for both Fabric public API and PBI private APIs
        """
        pass

    @property
    @abstractmethod
    def pbi_cluster_host(self) -> str:
        """
        The Scheme+Host of Fabric Public API
        e.g: https://api.fabric.microsoft.com
        """
        pass

    @property
    def artifact_context(self) -> Optional[ArtifactContext]:
        """
        Info of the notebook/sjd in execution.
        If it is not running in notebook/sjd, will be None
        """
        return None

    @property
    @abstractmethod
    def onelake_endpoint(self) -> str:
        """
        The URL of the Onelake endpoint, start with https://
        """
        pass

    """When allow_dynamic_resolution set to true, all below properties are resolved at runtime using workspace id, and you don't need implement it."""

    @property
    @abstractmethod
    def capacity_id(self) -> Optional[str]:
        """
        The id of capacity you operate on.
        """
        pass

    @property
    @abstractmethod
    def mwc_workload_host(self) -> Optional[str]:
        """
        The URL of the MWC workload host, start with https://
        This is optional since connect to private api (mwc workload) is not a must
        """
        return None


@inherit_docs
class IContextProviderPlugin(IContextProvider, IPlugin):
    pass
