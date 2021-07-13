import os

import requests
from vimeo_downloader import Vimeo
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.77.122:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.77.121:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.157:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.190:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.116:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.78.225:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.58:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.78.247:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.247:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.78.60:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.32:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.98:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.61:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.77:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.15.84:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.78.163:8000"}


# proxy = {"https": "http://3.130.124.100:8080"}
proxy = {"https": "http://dev:0@159.89.9.135:3128"}

# data1 = requests.get(url="https://www.indeed.com/")
# print(data1.status_code, data1.cookies)
# data = requests.get(url="https://www.careerbuilder.com/job/J301R0620YJ2PPJK564", proxies=proxy)
# data2 = requests.get(url="https://secure.indeed.com/account/login?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed"
#                          ".com%2Fhire&tmpl=desktop&from=gnav-util-employer--allspark--employer&_ga=2.159554805"
#                          ".935920425.1623929677-1957672176.1623830126", proxies=proxy)
# print(data.status_code)
# print(data2.status_code)
headers = {
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
    'X-CSRFToken': 'dfgdgdgdfgsdfgdsfg'
}
# data = requests.get("https://www.glassdoor.com/Job/director-jobs-SRCH_KO0,"
#                     "8.htm?jobType=fulltime&fromAge=7&minSalary=102200&includeNoSalaryJobs=true&maxSalary=186400",
#                     headers=headers)
# data = requests.get("https://vimeo.com/537780717")
# print(data.content)

# v = Vimeo('https://iframe.videodelivery.net/19a4a8c7357e4d21b8c65e341a179ab8/video/1080/init.mp4')
# s = v.streams
# print(s)
# best_stream = s[-1] # Select the best stream
# best_stream.download(download_directory='Downloads/', filename='video_example')

data = requests.get("https://iframe.videodelivery.net/1b0b934a-0a8f-4840-8b1d-9f33ec9238df")
print(data.text)
files = open(os.path.dirname(os.path.abspath(__file__)) + '/tmp/myfile.mp4', "wb")
files.write(data.content)
files.close()