import logging
import os
import sys
from abc import ABC
from logging import Handler
from typing import Any, List, Optional

from fabric.analytics.environment.base.log_handlers import (
    ILoggingHandlerProvider,
    ILoggingHandlerProviderPlugin,
)
from fabric.analytics.environment.base.plugin import IPlugin
from fabric.analytics.environment.constant import FABRIC_ANALYTICS_SDK_CONSOLE_LOG_LEVEL
from fabric.analytics.environment.plugin_provider import (
    BaseProvider,
    NoAvailableProvider,
)
from fabric.analytics.environment.utils.docstring import inherit_docs


class EnvLevelFilter(logging.Filter):
    def __init__(self, default="INFO"):
        super().__init__()
        self.env_var = FABRIC_ANALYTICS_SDK_CONSOLE_LOG_LEVEL
        self.default = default

    def filter(self, record):
        # Read environment variable *each time*
        level_name = os.getenv(self.env_var, self.default).upper()
        level = getattr(logging, level_name, logging.WARNING)
        return record.levelno >= level


@inherit_docs
class LoggingHandlerProvider(BaseProvider[ILoggingHandlerProviderPlugin]):
    """
    Provide Necessary Log Handler by selecting appropriate logging handler plugins.
    """

    plugin_entry_point_name = "fabric_analytics.logging_handler_provider"

    def __init__(self):
        BaseProvider.__init__(self)

    def get_handlers(self, **kwargs: Any) -> List[Handler]:
        """Get log handlers for current runtime.

        Returns:
            List[Handler]: list of log handlers available in current runtime
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        console_handler.addFilter(EnvLevelFilter())
        try:
            handlers: List[Handler] = [console_handler]
            handlers.extend(self.provider_plugin.get_handlers(**kwargs))
            return handlers
        except NoAvailableProvider:
            return [console_handler]

    def add_handlers(
        self,
        logger: logging.Logger,
        level=logging.DEBUG,
        formatter: Optional[logging.Formatter] = None,
        **kwargs: Any,
    ):
        """Attach environment handlers to logger.
        Please be aware the console log handler has default log level WARNING, and set logger log level DEBUG.
        To be able to see debug logs in console, set FABRIC_ANALYTICS_SDK_CONSOLE_LOG_LEVEL environment variable
        This allows log agent(mdsd) collecting logs for diagnostic purpose, while keeps stdout less verbose.
        Carefully set level to higher than debug level will make mdsd unable to collect debug log.

        Args:
            logger (logging.Logger): Your logger
            level (_type_, optional): log level. Defaults to logging.DEBUG.
            formatter (Optional[logging.Formatter], optional): custom formatter. Defaults to None.
        """
        for hdlr in self.get_handlers(**kwargs):
            if hdlr:
                if formatter:
                    hdlr.setFormatter(formatter)
                logger.addHandler(hdlr=hdlr)
        logger.setLevel(level)
        logger.propagate = False

    @property
    def provider_plugin(self) -> ILoggingHandlerProvider:
        return super().provider_plugin
