import os

TEST_MODE = os.getenv('TEST_MODE', default=False)

EXAMPLE_LINK = "https://www.glassdoor.com/Job/human-resources-jobs-SRCH_KO0,15.htm?jobType=fulltime&fromAge=7"
# ссылка на вакансию

if TEST_MODE == "True":
    TARGET_HOST = "http://127.0.0.1:8001"
else:
    TARGET_HOST = "https://www.glassdoor.com"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
                  'Safari/537.36',
    "authority": "www.glassdoor.com",
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
}

# List of vacancies in the left column

LEFT_COLUMN_V = {
    # parent block
    "parent_tag_name": "ul",
    "parent_tag_attr": "data-test",
    "parent_tag_attr_value": "jlGrid",
    # child blocks
    "tag_name": "li",
    "tag_attr": "data-is-easy-apply",
    "tag_attr_value": "true",
    # target link
    "tag_name_link": "a",
    "tag_attr_link": "data-test",
    "tag_attr_link_value": "job-link",
}

PAGINATE = {
    "tag_name": "div",
    "tag_attr": "data-test",
    "tag_attr_value": "page-x-of-y",
}
