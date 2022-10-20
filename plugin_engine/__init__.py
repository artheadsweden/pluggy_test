import pluggy
import importlib


class PluginEngine:
    def __init__(self, engine_name: str):
        self.plugins = []
        self._engine_name = engine_name
        self._pm = pluggy.PluginManager(self._engine_name)
        self.hookspecs = pluggy.HookspecMarker(self._engine_name)
        self.hookimpl = pluggy.HookimplMarker(self._engine_name)

    def register_plugin_module(self, module):
        self._pm.register(module)

    def register_plugin_module_by_path(self, module_path: str, required: bool=False):
        """Register hooks in a module with the PluginManager by Python path.

        Args:
            module_path (str): A Python dotted import path.
            manager (PluginManager): A pluggy plugin manager object to register this plugin to
            required (bool, optional): If False, ignore ImportError.
                Default: True.

        Returns:
            The imported module.

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

    def unregister(self, plugin_name):
        modules = [plugin for plugin in self.plugins if plugin['name'] == plugin_name]
        if len(modules) > 0:
            self._pm.unregister(modules[0]['plugin_module'])
            self.plugins = list(filter(lambda item: item['name'] != plugin_name, self.plugins))


    def get_hook(self):
        return self._pm.hook
        
