"""
Content analysis module
"""
from bs4 import BeautifulSoup as bs
import config
from botmodule import settings


class AnalyzerModule:

    def main_page(self, content: str) -> list:
        """
        Inbound page analyzer
        :param content: str
        :return: list
        """
        soup = bs(content, "html.parser")
        target_obj = soup.find(settings.TARGET_LIST["parent_tag"], class_=settings.TARGET_LIST["parent_class"])
        if target_obj:
            target_links = target_obj.find_all(settings.TARGET_LIST["child_tag"],
                                               class_=settings.TARGET_LIST["child_class"])
            if target_links:
                for link in target_links:
                    target = link.find(settings.TARGET_LIST["single_child"]["target_tag"],
                                       class_=settings.TARGET_LIST["single_child"]["target_class"])
                    print(target["href"])
        else:
            pass

        return list()
