import requests
from requests_html import HTMLSession

from botmodule import settings


class GetContent:

    def get_content(self, link: str):
        """
        Request page content for a given link.
        :param link: str
        :return:
        """
        response = ''
        session = HTMLSession()
        session.headers = settings.headers
        try:
            response = session.get(link)
            session.close()
        except requests.exceptions.RequestException as e:
            return {"status": False, "error": True, "status_code": response.status_code, "message": e}

        return {"status": True, "error": False, "status_code": response.status_code, "message": response.text}
