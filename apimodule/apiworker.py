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
        """
        Get file for download to form
        :param target_link: str
        :return:
        """
        url = config.SYSTEM_HOST + config.FILE_DOWNLOAD + '?name=' + target_link
        result = self.request.make_get(url)

        return result
