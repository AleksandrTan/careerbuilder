"""
Class for working with system api
"""
import requests

import config


class ApiWorker:

    def get_file(self, target_link):
        url = config.SYSTEM_HOST + config.FILE_DOWNLOAD + '?name=' + target_link
        r = requests.get(url)
        print(r.content)
