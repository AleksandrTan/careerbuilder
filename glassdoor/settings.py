EXAMPLE_LINK = "https://www.glassdoor.com/Job/director-jobs-SRCH_KO0," \
               "8.htm?jobType=fulltime&fromAge=7&minSalary=102200&includeNoSalaryJobs=true&maxSalary=186400"

TARGET_HOST = "https://www.glassdoor.com"

TEST_HOST = "http://127.0.0.1:8001"

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
