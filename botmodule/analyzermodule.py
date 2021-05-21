"""
Content analysis module
"""
from bs4 import BeautifulSoup as bs
import config
from botmodule import settings


class AnalyzerModule:

    def __init__(self):
        self.link_list = list()

    def main_page(self, content: str) -> dict:
        """
        Inbound page analyzer
        :param content: str
        :return: dict
        """
        soup = bs(content, "html.parser")
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
                        self.link_list.append(config.TARGET_HOST + target["href"])
                        continue
                    else:
                        continue

        # link to the first vacancy (button)

        if self.link_list:
            return {"status": True, "link_list": self.link_list}

        return {"status": False, "link_list": list()}
