# output stored in "result.json" file.

import re
import json
from bs4 import BeautifulSoup
import requests

client = requests.session()
headdash={'referrer':"https://targetstudy.com/school/12623/ajit-karam-singh-international-public-school-aksips/",'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def scrp(client,url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	r = client.get(url,headers=headers)
	return BeautifulSoup(str(r.content),"html.parser")


x = scrp(client,"https://targetstudy.com/school/schools-in-chandigarh.html")
y = [y for y in x.find_all("div") if y.has_attr('class') and y['class'][0] == "col-md-7"]
z = [z.a["href"] for z in y[0].find_all("div") if z.has_attr('class') and z['class'][0]=="\\'panel-footer\\'"]
state = x.find("h1").string.replace("Schools in", "").strip(" ")


def enumer(page,url,state):
	dici = {}
	for strin in page.table.contents:
		x = str(strin)
		if x.find("envelope") is not -1:
			dici["email"] = url
		elif x.find("home") is not -1:
			dici["address"] = strin.find_all("td")[1].get_text()
		elif x.find("phone") is not -1:
			dici["phone"] = strin.find_all("td")[1].get_text()
		elif x.find("mobile") is not -1:
			dici["mobile"] = strin.find_all("td")[1].get_text()

	dici["state"] = state
	dici["name"] = page.find("h1").get_text()
	return dici


r = [ enumer( scrp(client,r[2:-3]), r[2:-3], state) for r in z ]

with open('result.json', 'w') as fp:
    json.dump(r, fp)