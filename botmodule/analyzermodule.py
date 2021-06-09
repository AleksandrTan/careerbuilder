"""
Content analysis module
Use RequestModule to make requests to the target resource
"""
import time

from bs4 import BeautifulSoup as bs

import config
from botmodule import settings
from botmodule.requestmodule import RequestModule
from apimodule.proxy_work import ProxyWork


class AnalyzerModule:

    def __init__(self, order_id: str, link_id: str, user_name: str, last_name: str, email: str,
                 file_content, file_name, api_worker, proxy_worker: ProxyWork):
        """
        Возвращает либо ошибку о соедиенииб либо факт того, что ссылок для дальнейшего анализа не найдено
        :param proxy_worker: object
        :param order_id: str
        :param link_id: str
        :param user_name: str
        :param last_name: str
        :param email: str
        :param file_content: bytes
        """
        self.api_worker = api_worker
        self.proxy_worker = proxy_worker
        self.delay_requests = config.DELAY_REQUESTS
        self.file_name = file_name
        self.file_content = file_content
        self.user_name = user_name
        self.last_name = last_name
        self.email = email
        self.order_id = order_id
        self.link_id = link_id
        self.links_list = list()  # an array of links on the landing page
        self.button_links = list()  # an array of links to pages with a form to submit
        self.count_link = 0
        self.success_count_link = 0  # successfully sent links
        self.fail_count_link = 0  # unsuccessfully submitted links
        self.count_link_button = 0
        self.request = RequestModule(api_worker, proxy_worker)

    def parse_main_page(self, link: str) -> dict:
        """
        Select all job links used main link
        :param link:
        :return: dict
        """
        content = self.request.get_content(link, self.order_id)
        if not content["status"]:
            return content

        status = True
        reason = "connection"
        soup = bs(content["message"], "html.parser")
        # select all job links
        parent_obj = soup.find(settings.TARGET_LIST["parent_tag"], class_=settings.TARGET_LIST["parent_class"])
        if parent_obj:
            target_links = parent_obj.find_all(settings.TARGET_LIST["child_tag"],
                                               class_=settings.TARGET_LIST["child_class"])
            if target_links:
                for link in target_links:
                    target = link.find(settings.TARGET_LIST["single_child"]["target_tag"],
                                       class_=settings.TARGET_LIST["single_child"]["target_class"])
                    if target:
                        if config.TEST_MODE:
                            self.links_list.append(settings.TEST_HOST + target["href"])
                        else:
                            self.links_list.append(settings.TARGET_HOST + target["href"])
                        continue
                    else:
                        continue
                self.count_link = len(self.links_list)

        # get link to the first vacancy (button)
        button_link_parent = soup.find(settings.TARGET_BUTTON["parent_tag"],
                                       class_=settings.TARGET_BUTTON["parent_class"])
        if button_link_parent:
            button_link = button_link_parent.find(settings.TARGET_BUTTON["single_child"]["target_tag"],
                                                  class_=settings.TARGET_BUTTON["single_child"]["target_class"])

            if button_link and button_link.text == settings.TARGET_BUTTON["single_child"]["target_text"]:
                self.button_links.append(button_link["href"] + settings.TARGET_BUTTON["single_child"]["google_string"])
        if not self.links_list:
            # no links found
            status = False
            reason = "no_links"

        return {"status": status, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_button": self.count_link_button,
                "type_res": "analyzer_module", "reason": reason, "proxy":  tuple([self.proxy_worker.get_proxy_id(),
                                                                                  self.proxy_worker.get_proxy_dict()])}

    def parse_other_page(self) -> dict:
        """
        Go through all the links in the list
        and find a link to the submission form
        :return: dict
        """
        request_counter = 0
        status = True
        reason = "connection"
        for link in self.links_list:
            # update proxy server settings if needed
            if request_counter == config.NUMBER_REQUESTS:
                proxy = self.api_worker.update_proxy(self.proxy_worker.get_proxy_id(), False)
                if proxy:
                    # update proxy settings
                    self.proxy_worker.set_proxy_data(proxy[1], proxy[0])
                    request_counter = 0
            content = self.request.get_content(link, self.order_id)
            if not content["status"]:
                time.sleep(self.delay_requests)
                continue
            soup = bs(content["message"], "html.parser")
            # get link to the first vacancy (button)
            button_link_parent = soup.find(settings.TARGET_BUTTON["parent_tag"],
                                           class_=settings.TARGET_BUTTON["parent_class"])
            if button_link_parent:
                button_link = button_link_parent.find(settings.TARGET_BUTTON["single_child"]["target_tag"],
                                                      class_=settings.TARGET_BUTTON["single_child"]["target_class"])

                if button_link and button_link.text == settings.TARGET_BUTTON["single_child"]["target_text"]:
                    self.button_links.append(button_link["href"] +
                                             settings.TARGET_BUTTON["single_child"]["google_string"])
            request_counter += 1
            time.sleep(self.delay_requests)
        if not self.button_links:
            # no links found
            status = False
            reason = "no_links"

        return {"status": status, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_button": len(self.button_links),
                "type_res": "analyzer_module", "reason": reason}

    def form_page(self):
        """
        Open a page with a form, generate data, send form to the portal
        :return: None
        """
        request_counter = 0
        for button_link in self.button_links:
            # update proxy server settings if needed
            if request_counter == config.NUMBER_REQUESTS:
                proxy = self.api_worker.update_proxy(self.proxy_worker.get_proxy_id(), False)
                if proxy:
                    # update proxy settings
                    self.proxy_worker.set_proxy_data(proxy[1], proxy[0])
                    request_counter = 0
            content = self.request.get_content(button_link, self.order_id)
            # unsuccessfully submitted form
            if not content["status"]:
                self.fail_count_link += 1
                time.sleep(self.delay_requests)
                continue
            # prepare data for form
            data = self.get_data(content)
            send_status = self.send_data(data["url"], self.order_id, data["form"])
            # successfully submitted form
            if send_status["status"]:
                self.success_count_link += 1
            else:
                self.fail_count_link += 1
            time.sleep(self.delay_requests)
            request_counter += 1
            continue

        return {"status": True, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_button": len(self.button_links),
                "type_res": "analyzer_module", "reason": "reason", "success_count_link": self.success_count_link,
                "fail_count_link": self.fail_count_link}

    def get_data(self, contents) -> dict:
        # prepare form data
        form = dict()
        soup = bs(contents["message"], "html.parser")
        form["firstname"] = self.user_name
        form["lastname"] = self.last_name
        form["email"] = self.email
        form["cv_data"] = "SGVsbG8hCg=="
        form["cv_file_name"] = self.file_name
        form["upload_file"] = open(config.BASE_DIR + '/tmp/' + self.file_name, "rb")
        form["ai_resume_builder"] = False
        form["dropbox_cv_url"] = ''
        form["copy_paste"] = ''
        # set authenticity_token param
        authenticity_token_name = soup.find(settings.TARGET_FORM["authenticity_token"]["tag"],
                                            attrs={
                                                "name": settings.TARGET_FORM["authenticity_token"]["name_param"]
                                            }).get("content")
        authenticity_token_value = soup.find(settings.TARGET_FORM["authenticity_token"]["tag"],
                                             attrs={
                                                 "name": settings.TARGET_FORM["authenticity_token"]["name_value"]
                                             }).get("content")
        form[authenticity_token_name] = authenticity_token_value
        # set url param
        url = soup.find(settings.TARGET_FORM["parent_tag"],
                        attrs={"class": settings.TARGET_FORM["parent_class"]}).get("action")
        if config.TEST_MODE:
            url = settings.TEST_HOST + url
        else:
            url = settings.TARGET_HOST + url

        return {"form": form, "url": url}

    def send_data(self, url, order_id, data):
        result = self.request.send_data(url, order_id, data)
        return result
