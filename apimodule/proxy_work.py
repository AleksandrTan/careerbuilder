"""
Class for working with proxy servers
"""

class ProxyWork:

    def __init__(self):
        self.proxy_data = list()
        self.proxy_id = 0
        self.proxy_dict = dict()

    def set_proxy_data(self, proxy_dict: dict, proxy_id: int):
        """
        Set proxy
        :param proxy_dict: dict
        :param proxy_id: int
        :return:
        """
        self.proxy_data.clear()
        self.proxy_id = proxy_id
        self.proxy_dict = proxy_dict
        self.proxy_data.append(proxy_dict)
        self.proxy_data.append(proxy_id)

    def get_proxy_data(self) -> list :
        """
        Return list with proxy set
        :return: list
        """
        return self.proxy_data

    def get_proxy_id(self) -> int:
        """
        Return current proxy id
        :return: int
        """
        return self.proxy_id

    def get_proxy_dict(self) -> dict:
        """
        Return dict with proxy
        :return: dict
        """
        return self.proxy_dict
