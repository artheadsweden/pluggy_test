from plugin_engine import PluginEngine
import importlib


pe = PluginEngine('db_tester')


def main():
    pe.register_plugin_module_by_path('mongo_plugin')
    pe.register_plugin_module_by_path('mysql_plugin')
    pe.call.store_db(data={'id': 1, 'data': 'data, data, data'})
    
    pe.unplug('mysql_plugin')
    
    print('\t*** After unplug ***')
    pe.call.store_db(data={'id': 2, 'data': 'data, data, data'})


if __name__ == '__main__':
    main()