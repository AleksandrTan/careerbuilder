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

    def __init__(self):
        self.links_list = list()
        self.button_links = list()
        self.count_link = 0
        self.count_link_other = 0
        self.request = RequestModule()
        self.sender = SenderModule(self.request)

    def parse_main_page(self, link: str) -> dict:
        """
        Inbound page analyzer
        :param link:
        :return: dict
        """
        content = self.request.get_content(link)
        if not content["status"]:
            return content

        status = True
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
            status = False

        return {"status": status, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_other": self.count_link_other, "type_res": "analyzer_module"}

    def parse_other_page(self) -> dict:
        """
        Inbound page analyzer
        :return: dict
        """
        status = True
        for link in self.links_list:
            print(link)
            content = self.request.get_content(link)
            if not content["status"]:
                continue

            soup = bs(content["message"], "html.parser")

            # get link to the first vacancy (button)
            button_link_parent = soup.find(settings.TARGET_BUTTON["parent_tag"],
                                           class_=settings.TARGET_BUTTON["parent_class"])
            if button_link_parent:
                button_link = button_link_parent.find(settings.TARGET_BUTTON["single_child"]["target_tag"],
                                                      class_=settings.TARGET_BUTTON["single_child"]["target_class"])

                if button_link and button_link.text == settings.TARGET_BUTTON["single_child"]["target_text"]:
                    self.button_links.append(button_link["href"] + settings.TARGET_BUTTON["single_child"]["google_string"])
            time.sleep(2)

        return {"status": status, "link_list": self.links_list, "button_links": self.button_links,
                "count_link": self.count_link, "count_link_other": len(self.button_links),
                "type_res": "analyzer_module"}

    def form_page(self):
        print(self.button_links)
