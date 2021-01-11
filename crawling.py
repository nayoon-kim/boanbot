import requests
import json
from bs4 import BeautifulSoup

url = "https://www.boannews.com/Default.asp"
webpage = requests.get(url)
soup = BeautifulSoup(webpage.text, "html.parser")

headline_news = soup.select('#headline0 li')

result = {}
for i, mn in enumerate(headline_news):
    headline = "headline" + str(i+1)
    result[headline] = {}
    result[headline]["title"] = mn.text
    result[headline]["link"] = mn['onclick']

result_json = json.dumps(result, ensure_ascii=False)
# url

print(result_json)