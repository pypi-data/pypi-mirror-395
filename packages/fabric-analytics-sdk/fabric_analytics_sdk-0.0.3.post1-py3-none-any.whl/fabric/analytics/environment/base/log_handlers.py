import logging
import sys
from abc import ABC, abstractmethod
from logging import Handler
from typing import Any, List

from fabric.analytics.environment.base.plugin import IPlugin
from fabric.analytics.environment.utils.docstring import inherit_docs


class ILoggingHandlerProvider(ABC):
    @abstractmethod
    def get_handlers(self, **kwargs: Any) -> List[Handler]:
        pass


@inherit_docs
class ILoggingHandlerProviderPlugin(ILoggingHandlerProvider, IPlugin):
    pass
