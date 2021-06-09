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

    def get_proxy_data(self) -> list:
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

    def set_proxy(self, **data):
        """
        Init start proxy(self.proxies)
        :param data: dict
        :return: None
        """
        proxies = dict()
        if data["protocol_proxy"] and data["username_proxy"] and data["password_proxy"] and \
                data["host_proxy"] and data["port_proxy"]:
            proxies.update(
                {"https": data["protocol_proxy"] + "://" + data["username_proxy"] + ":" + data["password_proxy"] + "@" +
                          data["host_proxy"] + ":" + str(data["port_proxy"])})

        elif data["protocol_proxy"] and data["host_proxy"] and data["port_proxy"]:
            proxies.update(
                {"https": data["protocol_proxy"] + "://" + data["host_proxy"] + ":" + str(data["port_proxy"])})
        else:
            proxies.update({"https": "http://3.130.124.100:8080"})

        return proxies
