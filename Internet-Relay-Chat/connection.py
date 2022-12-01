import configparser


class Connection:
    """Get all the network details and connect the server and client"""

    def __init__(self, config_file_path):
        self.config_obj = configparser.ConfigParser()
        self.config_obj.read(config_file_path)
        self.nw_connection = self.config_obj['Network Connection']

    def get_host(self):
        return self.nw_connection['HOST']

    def get_port(self):
        return int(self.nw_connection['PORT'])
