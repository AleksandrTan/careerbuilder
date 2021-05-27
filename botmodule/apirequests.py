"""
Module for working with requests to a system api
"""
import requests


class ApiRequestModule:

    def make_get(self, url: str) -> dict:
        """
        :param url: str
        :return: dict
        """
        response = ''

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            return {"status": False, "error": True, "status_code": 0, "message": e, "type_res": "api_request_module"}

        except requests.exceptions.RequestException as e:
            return {"status": False, "error": True, "status_code": response.status_code, "message": e,
                    "type_res": "api_request_module"}

        return {"status": True, "error": False, "status_code": response.status_code, "message": response.text,
                "type_res": "api_request_module"}

    def make_post(self):
        pass
