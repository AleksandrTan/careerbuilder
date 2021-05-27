"""
Class for working with system api
"""
import requests

import config
from botmodule.apirequests import ApiRequestModule


class ApiWorker:
    def __init__(self):
        self.request = ApiRequestModule()

    def get_file(self, target_link):
        url = config.SYSTEM_HOST + config.FILE_DOWNLOAD + '?name=' + target_link
        r = self.request.make_get(url)
        return r
