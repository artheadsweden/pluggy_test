from plugin_engine import PluginEngine
import importlib


pe = PluginEngine('db_tester')


def main():
    pe.register_plugin_module(importlib.import_module('mongo_plugin'))
    pe.register_plugin_module(importlib.import_module('mysql_plugin'))
    pe.get_hook().store_db(data={'id': 1, 'data': 'data, data, data'})
    pe.unregister('db_plugins.mysql_plugin')
    print('\tafter unplug')
    pe.get_hook().store_db(data={'id': 2, 'data': 'data, data, data'})


if __name__ == '__main__':
    main()