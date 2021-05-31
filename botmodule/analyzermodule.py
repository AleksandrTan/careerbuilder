"""
Content analysis module
"""
import time

from bs4 import BeautifulSoup as bs

import config
from botmodule import settings
from botmodule.requestmodule import RequestModule
from botmodule.sendermodule import SenderModule


class AnalyzerModule:

    def __init__(self, proxy: dict, order_id: str, link_id: str, user_name: str, last_name: str, email: str,
                 file_content, file_name):
        """
        Возвращает либо ошибку о соедиенииб либо факт того, что ссылок для дальнейшего анализа не найдено
        :param proxy: dict
        :param order_id: str
        :param link_id: str
        :param user_name: str
        :param last_name: str
        :param email: str
        :param file_content: bytes
        """
        self.file_name = file_name
        self.file_content = file_content
        self.user_name = user_name
        self.last_name = last_name
        self.email = email
        self.proxy = proxy
        self.order_id = order_id
        self.link_id = link_id
        self.links_list = list()  # an array of links on the landing page
        self.button_links = list()  # an array of links to pages with a form to submit
        self.count_link = 0
        self.count_link_other = 0
        self.request = RequestModule()
        self.sender = SenderModule(self.request)

    def parse_main_page(self, link: str) -> dict:
        """
        Select all job links
        :param link:
        :return: dict
        """
        content = self.request.get_content(link, self.proxy, self.order_id)
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
                            self.links_list.append(config.TEST_HOST + target["href"])
                        else:
                            self.links_list.append(config.TARGET_HOST + target["href"])
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
                "count_link": self.count_link, "count_link_other": self.count_link_other,
                "type_res": "analyzer_module", "reason": reason}

    def parse_other_page(self) -> dict:
        """
        Go through all the links in the list
        and find a link to the submission form
        :return: dict
        """
        status = True
        reason = "connection"
        for link in self.links_list:
            print(link)
            content = self.request.get_content(link, self.proxy, self.order_id)
            if not content["status"]:
                time.sleep(5)
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
            # time.sleep(5)
        if not self.button_links:
            # no links found
            status = False
            reason = "no_links"

        return {"status": status, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_other": len(self.button_links),
                "type_res": "analyzer_module", "reason": reason}

    def form_page(self):
        """
        Open a page with a form, generate data, send to the portal
        :return:
        """
        for button_link in self.button_links:
            content = self.request.get_content(button_link, self.proxy, self.order_id)
            if not content["status"]:
                time.sleep(5)
                continue
            data = self.get_data(content)
            send_status = self.send_data(data["url"], self.proxy, self.order_id, data["form"])
            print(send_status)

        # print(self.button_links)

    def get_data(self, contents) -> dict:
        # prepare form data
        form = dict()
        soup = bs(contents["message"], "html.parser")
        form["firstname"] = self.user_name
        form["lastname"] = self.last_name
        form["email"] = self.email
        form["cv_data"] = "SGVsbG8hCg=="
        form["cv_file_name"] = self.file_name

        binary_file = open(self.file_name, "wb")
        form["upload_file"] = binary_file.write(self.file_content)
        # binary_file.close()

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
            url = config.TEST_HOST + url
        else:
            url = config.TARGET_HOST + url

        return {"form": form, "url": url}

    def send_data(self, url, proxy, order_id, data):
        result = self.request.send_data(url, proxy, order_id, data)
        return result
