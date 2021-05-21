"""
Content analysis module
"""
from bs4 import BeautifulSoup as bs

import config
from botmodule import settings
from botmodule.requestmodule import RequestModule


class AnalyzerModule:

    def __init__(self):
        self.links_list = list()
        self.button_links = list()
        self.count_link_list = 0
        self.request = RequestModule()

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
                self.count_link_list = len(self.links_list)

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
                "count_link_list": self.count_link_list, "type_res": "analyzer_module"}

    def parse_other_page(self, link_list: str) -> dict:
        """
        Inbound page analyzer
        :param link_list:
        :return: dict
        """
        content = self.request.get_content(link_list)
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
                        self.links_list.append(config.TARGET_HOST + target["href"])
                        continue
                    else:
                        continue
                self.count_link_list = len(self.links_list)

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
                "count_link_list": self.count_link_list, "type_res": "analyzer_module"}
