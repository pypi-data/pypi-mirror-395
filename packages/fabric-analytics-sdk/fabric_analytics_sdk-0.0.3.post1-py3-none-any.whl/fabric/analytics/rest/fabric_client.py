import logging
import uuid
from typing import TYPE_CHECKING, Any, Optional

from azure.core.credentials import TokenCredential
from azure.core.pipeline.policies import RetryPolicy
from azure.core.pipeline.transport import RequestsTransport
from azure.core.rest import HttpRequest, HttpResponse
from fabric.analytics.environment.constant import PBI_SCOPE_PPE
from fabric.analytics.environment.context import FabricContext
from fabric.analytics.environment.credentials import FabricAnalyticsTokenCredentials
from fabric.analytics.rest._generated._client import BaseFabricRestClient
from fabric.analytics.rest.client_extension import _FabricRestAPIExtension
from fabric.analytics.rest.policies import CustomHttpLoggingPolicy

from ..version import VERSION

logger = logging.getLogger(__name__)


class FabricRestClient(BaseFabricRestClient, _FabricRestAPIExtension):
    def __init__(
        self,
        credential: Optional[TokenCredential] = None,
        **kwargs: Any,
    ):
        """_summary_

        Args:
            credential (Optional[TokenCredential], optional): Defaults to FabricAnalyticsTokenCredentials(**kwargs).
            is_ppe: Defaults to FabricContext().internal_context.is_ppe()
            ednpoint: Defaults to FabricContext().pbi_cluster_host, you don't need to set this if you pass endpoint in actual call
        """
        kwargs.setdefault("sdk_moniker", "fabric-analytics-sdk/{}".format(VERSION))
        endpoint = kwargs.pop("endpoint", None) or FabricContext().pbi_shared_host
        is_ppe = kwargs.get("is_ppe", FabricContext().internal_context.is_ppe())
        kwargs.setdefault("use_ml_1p", True)

        if is_ppe:
            kwargs.setdefault(
                "is_ppe", is_ppe
            )  # Token provider use this to decide app_id
            kwargs.setdefault(
                "credential_scopes",
                [PBI_SCOPE_PPE],
            )  # This is requried, client use this scope by default

        if not credential:
            credential = FabricAnalyticsTokenCredentials(**kwargs)

        if "http_logging_policy" not in kwargs:
            kwargs["http_logging_policy"] = CustomHttpLoggingPolicy(
                logger=logger, **kwargs
            )

        if "transport" not in kwargs:
            kwargs["transport"] = RequestsTransport(
                connection_timeout=30, read_timeout=30
            )

        if "retry_policy" not in kwargs:
            kwargs["retry_policy"] = RetryPolicy(retry_total=0)

        super().__init__(
            endpoint=endpoint,
            credential=credential,
            **kwargs,
        )

    def send_request(
        self, request: HttpRequest, *, stream: bool = False, **kwargs: Any
    ) -> HttpResponse:
        if "ActivityId" not in request.headers:
            request.headers["ActivityId"] = str(uuid.uuid4())

        try:
            return super().send_request(request=request, stream=stream, **kwargs)
        except Exception as e:
            logger.error(
                f"Exception {e} sending request {request.url}, ClientActivityId: {request.headers.get('ActivityId')}"
            )
            raise e
