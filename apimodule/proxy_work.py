class ProxyWork:

    def __init__(self):
        print(3500)
        self.proxy_data = list()
        self.proxy_id = 0
        self.proxy_dict = dict()

    def set_proxy_data(self, proxy_dict: dict, proxy_id: int):
        self.proxy_id = proxy_id
        self.proxy_dict = proxy_dict
        self.proxy_data.append(proxy_dict)
        self.proxy_data.append(proxy_id)

    def get_proxy_data(self):
        return self.proxy_data

    def get_proxy_id(self):
        return self.proxy_id

    def get_proxy_dict(self):
        return self.proxy_dict
