import requests

proxy = {

         "http": "http://2DxLL0:fwcZsa@138.219.173.104:8000"}
data = requests.get(url="https://www.careerbuilder.com/job/J301R0620YJ2PPJK564", proxies=proxy)
print(data.status_code)
