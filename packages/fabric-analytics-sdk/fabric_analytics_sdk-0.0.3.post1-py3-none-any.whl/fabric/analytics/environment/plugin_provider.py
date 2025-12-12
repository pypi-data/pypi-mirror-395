import logging
from typing import Generic, List, Optional, TypeVar

from fabric.analytics.environment.base.plugin import IPlugin
from fabric.analytics.environment.utils.plugins import get_entry_points
from fabric.analytics.environment.utils.singleton import Singleton

T = TypeVar("T", bound=IPlugin)
logger = logging.getLogger(__name__)


class NoAvailableProvider(Exception):
    pass


class BaseProvider(Generic[T], metaclass=Singleton):
    plugin_entry_point_name = "fabric_analytics.base"

    def __init__(self):
        self._provider_plugin: Optional[T] = None
        self._registry: List[T] = []
        return

    def register(self, provider_cls: T):
        """
        Register an provider class as candidate
        """
        for existing_cls in self._registry:
            if existing_cls is provider_cls:
                return

        self._registry.append(provider_cls)

    def unregister(self, provider_cls: T) -> bool:
        """
        unregister an provider class as candidate, remove any initialized instance

        returns whether provider_cls is in _registry list.
        """
        provider_cls_in_registry = provider_cls in self._registry
        if provider_cls_in_registry:
            self._registry.remove(provider_cls)
        if isinstance(self._provider_plugin, provider_cls):
            self._provider_plugin = None

        return provider_cls_in_registry

    def set_provider_plugin(self, provider_plugin: T):
        """
        A name friendly method override internal provider plugin with provided instance
        """
        self._provider_plugin = provider_plugin

    def _register_entrypoints(self):
        """Register plugin provider implemented by other packages"""
        for entrypoint in get_entry_points(self.plugin_entry_point_name):
            try:
                self.register(entrypoint.load())
            except (AttributeError, ImportError) as exc:
                logger.exception(
                    f"Failure attempting to register {self.plugin_entry_point_name} provider"
                    + f'provider "{entrypoint.name}": {exc}',
                    stacklevel=2,
                )

    @property
    def provider_plugin(self) -> T:
        """
        Get provider plugin. It will search entrypoint to create one if current is None
        """
        if self._provider_plugin:
            return self._provider_plugin

        self._register_entrypoints()
        providers_in_context: List[T] = []

        for provider in self._registry:
            try:
                if provider.in_context():
                    providers_in_context.append(provider)
            except Exception as e:
                logger.warning(
                    "Encountered unexpected error during resolving provider: %s", e
                )

        # sort by priority (ascending = low to high, 255 means default)
        providers_in_context = sorted(providers_in_context, key=lambda p: p.priority)

        if len(providers_in_context) == 0:
            raise NoAvailableProvider(f"lack of valid {self.__class__.__name__}")
        elif len(providers_in_context) > 1 and providers_in_context[1].priority != 255:
            # it is common for environmental plugin to override default plugin, but more than one non default plugin is problematic
            logger.warning(
                f"more than one context provider except the default provider available for current environment {providers_in_context}"
            )

        logger.debug(f"initializing {provider} as {self.__class__.__name__}")
        self._provider_plugin = providers_in_context[0]()
        assert self._provider_plugin is not None
        return self._provider_plugin
