TARGET_HOST = "https://www.careerbuilder.com"
TEST_HOST = "http://127.0.0.1:8000"
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

cookies = {

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
