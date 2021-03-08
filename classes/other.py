from samp_client.client import SampClient
from samp_client.exceptions import ConnectionError


class Other:

    # Get server info
    @staticmethod
    def get_server_info():
        try:
            server = SampClient(address='45.153.231.35', port=7777).connect()
            server_info = server.get_server_info()
        except ConnectionError and TypeError:
            server_info = None
        return server_info
