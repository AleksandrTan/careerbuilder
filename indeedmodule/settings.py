import os

user = "rumych2021@ukr.net"
password = "ufeltfvec"
TEST_MODE = os.getenv('TEST_MODE', default=False)
TEST_HOST = "http://127.0.0.1:8001"
TARGET_HOST = "https://www.indeed.com/"
if TEST_MODE == "True":
    LOGIN_PAGE = "http://127.0.0.1:8001/mainsystem/testauthpageindeed/"
else:
    LOGIN_PAGE = "https://secure.indeed.com/account/login?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2Fhire" \
             "&tmpl=desktop&from=gnav-util-employer--allspark--employer&_ga=2.159554805.935920425.1623929677" \
             "-1957672176.1623830126"

LOGIN_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "secure.indeed.com",
    "Pragma": "no-cache",
    "Referer": "https://www.indeed.com/",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 "
                  "Safari/537.36 "
}

LOGIN_COOKIES = {
    "device": "b306ea4029f29481220b6f8aa6c1274b",
    "fbredirect": "/account/register",
    "APPLE_N": "80UurDIR01hkYWWE",
    "G_ENABLED_IDPS": "google",
    "LANG": "en_US",
    "preExtAuthParams": "co=US&continue=https%3A%2F%2Fwww.indeed.com%2Fjobs%3Fq%3Dpython%26jt%3Dfulltime%26"
                        "taxo1%3D8GQeqOBVSO2eVhu55t0BMg&employer=true&form_tk=1f8f19k8aocb1800&"
                        "from=gnav-util-jobsearch--jasx&hl=en_US&service=my&surftok=wIxZ2FUlwZTbqkAIuzF0WxwU0MJp292h",
    "conf_snt": 1,
    "PPDM": "my=https%3A%2F%2Femployers.indeed.com&draw=https%3A%2F%2Femployers.indeed.com"
}
"""
Login form fields
"""
LOGIN_FORM_TAGS = {
    "parent_tag": "form",
    "parent_id": "loginform",
    "input_tag_hidden": "input",
    "input_tag_type_hidden": "hidden",
}

"""
Number of vacancies by reference. Used for pagination.
"""
COUNT_VACANCY = {
    "parent_tag": "div",
    "target_id": "searchCountPages"
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
