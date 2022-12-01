import configparser


config = configparser.ConfigParser()

"""Builds structure for the INI file that is going to be generated"""
config.add_section('Network Connection')
config.set('Network Connection', 'HOST', '127.0.0.1')
config.set('Network Connection', 'PORT', '65000')

"""Writes the structure to the new INI file in the given location"""
with open(r'app_config_file.ini', 'w') as configfile:
    config.write(configfile)
