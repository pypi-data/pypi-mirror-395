import logging
import os

from azure.core.pipeline import PipelineRequest, PipelineResponse, policies
from azure.core.pipeline.policies import HttpLoggingPolicy
from azure.core.pipeline.policies._universal import HTTPRequestType, HTTPResponseType

logger = logging.getLogger(__name__)


class CustomHttpLoggingPolicy(policies.HttpLoggingPolicy):
    DEFAULT_HEADERS_ALLOWLIST = policies.HttpLoggingPolicy.DEFAULT_HEADERS_ALLOWLIST | {
        "RequestId",
        "Requestid",
        "requestId",
        "x-ms-root-activity-id",
        "ActivityId",
    }

    def on_response(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: PipelineResponse[HTTPRequestType, HTTPResponseType],
    ) -> None:
        http_response = response.http_response

        # Get logger in my context first (request has been retried)
        # then read from kwargs (pop if that's the case)
        # then use my instance logger
        # If on_request was called, should always read from context
        options = request.context.options
        custom_logger = request.context.setdefault(
            "logger", options.pop("logger", logger)
        )

        try:
            if (
                response.http_response.status_code > 400
                and response.http_response.status_code != 404
                # 400 and 404 logs are in debug level
            ):
                custom_logger.warning(
                    f"Error response returned, request: {request.http_request.url}, ClientActivityId {request.http_request.headers.get('ActivityId')}"
                )
                log_method = custom_logger.warning
            else:
                log_method = custom_logger.debug

            if log_method == custom_logger.debug and not custom_logger.isEnabledFor(
                logging.DEBUG
            ):
                return

            multi_record = os.environ.get(HttpLoggingPolicy.MULTI_RECORD_LOG, False)
            if multi_record:
                log_method("Response status: %r", http_response.status_code)
                log_method("Response headers:")
                for res_header, value in http_response.headers.items():
                    value = self._redact_header(res_header, value)
                    log_method("    %r: %r", res_header, value)
                return
            log_string = "Response status: {}".format(http_response.status_code)
            log_string += "\nResponse headers:"
            for res_header, value in http_response.headers.items():
                value = self._redact_header(res_header, value)
                log_string += "\n    '{}': '{}'".format(res_header, value)
            log_method(log_string)
        except Exception as err:  # pylint: disable=broad-except
            custom_logger.warning("Failed to log response: %s", repr(err))
