import requests

# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.77.122:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.77.121:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.157:8000"}
# proxy = {"https": "http://2DxLL0:fwcZsa@196.17.76.190:8000"}
proxy = {"https": "http://2DxLL0:fwcZsa@196.17.79.116:8000"}
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
print(data.status_code)
