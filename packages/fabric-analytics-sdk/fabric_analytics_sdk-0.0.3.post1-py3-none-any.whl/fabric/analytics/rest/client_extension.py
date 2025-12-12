from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, AsyncIterable, Dict, Iterable, MutableMapping, Optional, Union

from azure.core.rest import HttpRequest, HttpResponse
from azure.core.rest._helpers import FilesType, ParamsType

ContentType = Union[str, bytes, Iterable[bytes], AsyncIterable[bytes]]


class _FabricRestAPIExtension(ABC):
    """
    Fabric Rest API Client designed for all pbi/fabric rest api calls
    ref: azure.storage.blob._generated._azure_blob_stroage AzureBlobStorage
    """

    @abstractmethod
    def send_request(
        self, request: HttpRequest, *, stream: bool = False, **kwargs: Any
    ) -> HttpResponse:
        pass

    def get(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> "HttpResponse":
        """Create a GET request object.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "GET",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def put(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Send a PUT request.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :param stream_content: The body content as a stream
        :type stream_content: stream or generator or asyncgenerator
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "PUT",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def post(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Send a POST request.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :param stream_content: The body content as a stream
        :type stream_content: stream or generator or asyncgenerator
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "POST",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def head(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Send a HEAD request.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :param stream_content: The body content as a stream
        :type stream_content: stream or generator or asyncgenerator
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "HEAD",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def patch(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Send a PATCH request.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :param stream_content: The body content as a stream
        :type stream_content: stream or generator or asyncgenerator
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "PATCH",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def delete(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Send a DELETE request.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "DELETE",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def merge(
        self,
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Create a MERGE request object.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :param content: The body content
        :type content: bytes or str or dict
        :param dict form_content: Form content
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "MERGE",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)

    def options(
        self,  # pylint: disable=unused-argument
        url: str,
        *,
        params: Optional[ParamsType] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        content: Optional[ContentType] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[FilesType] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> HttpResponse:
        """Create a OPTIONS request object.

        :param str url: The request URL.
        :param dict params: Request URL parameters.
        :param dict headers: Headers
        :keyword content: The body content
        :type content: bytes or str or dict
        :keyword dict form_content: Form content
        :return: An HttpRequest object
        :rtype: ~azure.core.pipeline.transport.HttpRequest
        """
        request = HttpRequest(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
        )
        return self.send_request(request, stream=stream, **kwargs)
