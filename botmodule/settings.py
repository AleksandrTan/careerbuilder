TARGET_HOST = "https://www.careerbuilder.com"
TEST_HOST = "http://127.0.0.1:8001"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
                  'Safari/537.36',
    "authority": "www.careerbuilder.com",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    'X-CSRFToken': 'dfgdgdgdfgsdfgdsfg'
}

"""
List of links to vacancies
"""
TARGET_LIST = {
    "parent_tag": "div",
    "parent_class": "data-results fix-elem-content nav-tabs",
    "child_tag": "div",
    "child_class": "data-results-content-parent relative",
    "single_child": {
        "target_tag": "a",
        "target_class": "data-results-content block job-listing-item",
        "target_attr": "href"
    }
}

"""
Button to go to the form submit page
"""
TARGET_BUTTON = {
    "parent_tag": "div",
    "parent_class": "data-display-header_info-apply dib-m",
    "single_child": {
        "target_tag": "a",
        "target_class": "btn btn-linear btn-linear-green btn-block internal-apply-cta",
        "target_attr": "href",
        "target_text": "Apply Now",
        "target_text_company": "Apply on company site",
        "google_string": "?&_ga=2.137065200.1557281988.1621516955-535983977.1621516955"
    }
}

"""
Form
"""
TARGET_FORM = {
    "parent_tag": "form",
    "parent_class": "form-material resume_upload",
    "authenticity_token": {
        "tag": "meta",
        "name_param": "csrf-param",
        "name_value": "csrf-token"
    }
}

# Messages to log file and console
MESSAGES_LOG = {
    "no_auth_data": {"message": "Order - order. Attention! Authorization data not installed! Check the presence of a "
                                "email and password when creating a task!!!\n"},
    "main_page_fail": {"message": "Order - order. Attention! Authorization data not installed! Check the presence of a "
                                  "email and password when creating a task!!!\n"},
    "fail_login": {"message": "Order - order. Attention! Login procedure aborted.!\n"},
    "fail_login_form": {"message": "Order - order. Attention! Login form not found or the source code of the target "
                                   "portal page has been changed..!\n"},
    "fail_send_login_form": {"message": "Order - order. Attention!Login form data failed validation.\n"},

    "target_connect_error": {"message": "Order - order. Attention! Target resource is not responding! message code\n"},
    "api_connect_error": {"message": "Attention! The system api is not responding! message code\n"},
    "no_file": {"message": "Order - order. Mailing file not found.\n"},
    "main_content_error": {"message": "Order - order. When Requesting a start link, the target resource did not "
                                      "respond correctly!Perhaps the proxy server did not respond in time. code "
                                      "message\n"},
    "no_links_found": {"message": "Order - order. An error occurred while executing the task. No links found on the "
                                  "main page. The target resource may have changed the source code!\n"},

    "no_button_found": {"message": "Order - order. An error occurred while executing the task. No links to form pages "
                                   "were found. The target resource may have changed the source code!\n"}
}

MESSAGES_ERROR_API = {
    "no_auth_data": {"message": "Order - order. Attention! Authorization data not installed! Check the presence of a "
                                "email and password when creating a task!!!\n"},
    "main_page_fail": {"message": "Order - order. Attention! Authorization data not installed! Check the presence of a "
                                  "email and password when creating a task!!!\n"},
    "fail_login": {"message": "Order - order. Attention! Login procedure aborted.!\n Messages - "
                              "message \n Proxy - proxy\n"},
    "fail_login_form": {"message": "Order - order. Attention! Login form not found or the source code of the target "
                                   "portal page has been changed..!\n"},
    "fail_send_login_form": {"message": "Order - order. url Attention!Login form failed validation.\n "
                                        "status_code message"},
    "no_file": {
        "message": "Mailing file not found."
    },
    "target_connect_error": {
        "message": "Attention! Target resource is not responding! If code 403 - Perhaps the proxy server did not "
                   "respond in time. \n Code - status_code \n Messages - message \n Proxy - pserver\n"
    },
    "no_links_found": {"message": "An error occurred while executing the task. No links found on the "
                                  "main page. The target resource may have changed the source code!\n"},
    "no_button_found": {"message": "An error occurred while executing the task. No links to form pages were found. "
                                   "The target resource may have changed the source code!"}
}
