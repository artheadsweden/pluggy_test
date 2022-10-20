import pluggy
import importlib
from types import ModuleType


class PluginEngine:
    def __init__(self, engine_name: str):
        self.plugins = []
        self._engine_name = engine_name
        self._pm = pluggy.PluginManager(self._engine_name)
        # Not sure about the role of hookspecs. Seems to work without it
        # self.hookspecs = pluggy.HookspecMarker(self._engine_name)
        self.hookimpl = pluggy.HookimplMarker(self._engine_name)

    def register_plugin_module(self, module: ModuleType):
        """
        Register a hook by passing the imported module.

        Args:
            module (ModuleType): The module containing the hook
        Returns:
            None
        """
        self.plugins.append(
            {
                # TODO: Does this work if plugin is in a package? Probably not
                'name': module.__name__,
                'plugin_module': module
            }
        )

        self._pm.register(module)

    def register_plugin_module_by_path(self, module_path: str, required: bool=False):
        """
        Register a hook by passing a Python path.

        Args:
            module_path (str): A Python dotted import path.
            required (bool, optional): If False, ignore ImportError. Default: True.

        Returns:
            None

        Raises:
            ImportError: If `required` is True and the module cannot be imported.
        """
        
        try:
            module = importlib.import_module(module_path)
            self.plugins.append(
                {
                    'name': module_path,
                    'plugin_module': module
                }
            )
        except ImportError:
            if required:
                raise
        else:
            self._pm.register(module)

    def unplug(self, plugin_name: str):
        """"
        Unregisters a plugin.

        Args:
            plugin_name (str): The name used to register the plugin

        Returns:
            None
        """
        modules = [plugin for plugin in self.plugins if plugin['name'] == plugin_name]
        if len(modules) > 0:
            self._pm.unregister(modules[0]['plugin_module'])
            self.plugins = list(filter(lambda item: item['name'] != plugin_name, self.plugins))
        else:
            print(self.plugins)
            raise RuntimeError(f'No module named {plugin_name} registered.')

    @property
    def call(self):
        """
        Property that can be used to call the hooks
        """
        return self._pm.hook
        
