import time
from typing import TYPE_CHECKING, Any, MutableMapping, Optional, TypeVar

from azure.core.exceptions import ServiceRequestError
from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.policies import HTTPPolicy
from azure.core.pipeline.transport import HttpRequest
from azure.core.pipeline.transport import HttpRequest as LegacyHttpRequest
from azure.core.pipeline.transport import HttpResponse as LegacyHttpResponse
from azure.core.rest import HttpRequest, HttpResponse

from .credentials import decode_jwt

if TYPE_CHECKING:
    from fabric.analytics.environment.base.credentials import (
        IFabricAnalyticsMWCCredential,
        MwcAccessToken,
        MWCTokenRequestPayload,
    )

HTTPRequestType = TypeVar("HTTPRequestType", HttpRequest, LegacyHttpRequest)
HTTPResponseType = TypeVar("HTTPResponseType", HttpResponse, LegacyHttpResponse)


# pylint:disable=too-few-public-methods
class _MWCCredentialPolicyBase:
    """Base class for a MWC Token Credential Policy.
    To avoid you mix up token with different payload, the mwc token request payload doesn't allow modification after you create the object

    :param credential: The credential.
    :type credential: ~fabric.analytics.environment.base.credentials.IFabricAnalyticsMWCCredential
    """

    def __init__(
        self,
        credential: "IFabricAnalyticsMWCCredential",
        **kwargs: Any,
    ) -> None:
        super(_MWCCredentialPolicyBase, self).__init__()
        self._credential = credential
        self._token: "MwcAccessToken" = None

    @staticmethod
    def _enforce_https(request: PipelineRequest[HTTPRequestType]) -> None:
        # move 'enforce_https' from options to context so it persists
        # across retries but isn't passed to a transport implementation
        option = request.context.options.pop("enforce_https", None)

        # True is the default setting; we needn't preserve an explicit opt in to the default behavior
        if option is False:
            request.context["enforce_https"] = option

        enforce_https = request.context.get("enforce_https", True)
        if enforce_https and not request.http_request.url.lower().startswith("https"):
            raise ServiceRequestError(
                "MWC token authentication is not permitted for non-TLS protected (non-https) URLs."
            )

    @staticmethod
    def _update_headers(headers: MutableMapping[str, str], token: str) -> None:
        """Updates the Authorization header with the bearer token.

        :param MutableMapping[str, str] headers: The HTTP Request headers
        :param str token: The OAuth token.
        """
        headers["Authorization"] = "mwctoken {}".format(token)

    @property
    def _need_new_token(self) -> bool:
        now = time.time()
        refresh_on = self._token.refresh_on
        return (
            not self._token
            or (refresh_on and refresh_on <= now)
            or self._token.expires_on - now < 300
        )

    def _request_token(self) -> "MwcAccessToken":
        """Request a new token from the credential.

        This will call the credential's appropriate method to get a token and store it in the policy.

        :param str scopes: The type of access needed.
        """
        self._token = self._credential.get_mwc_token()


class MWCTokenCredentialPolicy(
    _MWCCredentialPolicyBase, HTTPPolicy[HTTPRequestType, HTTPResponseType]
):
    """Adds a bearer token Authorization header to requests.

    :param credential: The credential.
    :type credential: ~azure.core.TokenCredential
    :param str scopes: Lets you specify the type of access needed.
    :keyword bool enable_cae: Indicates whether to enable Continuous Access Evaluation (CAE) on all requested
        tokens. Defaults to False.
    :raises: :class:`~azure.core.exceptions.ServiceRequestError`
    """

    def on_request(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Called before the policy sends a request.

        The base implementation authorizes the request with a bearer token.

        :param ~azure.core.pipeline.PipelineRequest request: the request
        """
        self._enforce_https(request)
        if self._token is None or self._need_new_token:
            self._request_token()
        mwc_token = self._token.token.Token
        self._update_headers(request.http_request.headers, mwc_token)

    def authorize_request(
        self, request: PipelineRequest[HTTPRequestType], *scopes: str, **kwargs: Any
    ) -> None:
        """Acquire a token from the credential and authorize the request with it.

        Keyword arguments are passed to the credential's get_token method. The token will be cached and used to
        authorize future requests.

        :param ~azure.core.pipeline.PipelineRequest request: the request
        :param str scopes: required scopes of authentication
        """
        self._request_token(*scopes, **kwargs)
        mwc_token = self._token.token.Token
        self._update_headers(request.http_request.headers, mwc_token)

    def send(
        self, request: PipelineRequest[HTTPRequestType]
    ) -> PipelineResponse[HTTPRequestType, HTTPResponseType]:
        """Authorize request with a bearer token and send it to the next policy

        :param request: The pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        :return: The pipeline response object
        :rtype: ~azure.core.pipeline.PipelineResponse
        """
        self.on_request(request)
        try:
            response = self.next.send(request)
        except Exception:
            self.on_exception(request)
            raise

        self.on_response(request, response)
        if response.http_response.status_code == 401:
            self._token = None  # any cached token is invalid

        return response

    def on_response(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: PipelineResponse[HTTPRequestType, HTTPResponseType],
    ) -> None:
        """Executed after the request comes back from the next policy.

        :param request: Request to be modified after returning from the policy.
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: Pipeline response object
        :type response: ~azure.core.pipeline.PipelineResponse
        """

    def on_exception(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Executed when an exception is raised while executing the next policy.

        This method is executed inside the exception handler.

        :param request: The Pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        # pylint: disable=unused-argument
        return
