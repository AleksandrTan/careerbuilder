import requests

proxy = {"https": "http://2DxLL0:fwcZsa@196.17.77.122:8000"}
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

data1 = requests.get(url="http://www.freeproxylists.net/ru/", proxies=proxy)
print(data1.status_code)
data = requests.get(url="https://www.careerbuilder.com/job/J301R0620YJ2PPJK564", proxies=proxy)
data2 = requests.get(url="https://secure.indeed.com/account/login?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed"
                         ".com%2Fhire&tmpl=desktop&from=gnav-util-employer--allspark--employer&_ga=2.159554805"
                         ".935920425.1623929677-1957672176.1623830126", proxies=proxy)
print(data.status_code)
print(data2.status_code)
