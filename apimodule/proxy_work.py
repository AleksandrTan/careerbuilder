"""
Class for working with proxy servers
"""


class ProxyWork:

    def __init__(self, data):
        self.proxy_data = list()
        self.proxy_id = 0
        self.proxy_dict = dict()
        self.host_proxy = data["host"]
        self.port_proxy = data["port"]
        self.username_proxy = data["username"]
        self.password_proxy = data["password"]

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

    def get_manifest_json(self):
        return """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

    def get_background_js(self):
        return """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                          singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                          },
                          bypassList: ["localhost"]
                        }
                      };
                
                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
                
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }
                """ % (self.host_proxy, self.port_proxy, self.username_proxy, self.password_proxy)
