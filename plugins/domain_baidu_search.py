#! -*- coding:utf-8 -*-

__author__="nMask"
__Date__="1 Jul 2019"
__Blog__="https://thief.one"
__version__="1.0"
__py_version__="2.7.11"


import random
import urlparse
from bs4 import BeautifulSoup
import gevent
from gevent import monkey, pool
monkey.patch_all()
import requests

headers = {
	
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,mt;q=0.7,zh-TW;q=0.6",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "BAIDUID=9F8F8C5499E080B4D41BFDA21C4095ED:FG=1; BIDUPSID=9F8F8C5499E080B4D41BFDA21C4095ED; PSTM=1535951702; BD_UPN=123253; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02922665266; ispeed_lsm=0; MCITY=-%3A; H_PS_PSSID=1441_27213_21095_27245_27509; BDSFRCVID=R14sJeCCxG3i7nb7N48th_edM8CH6AQX2liC3J; H_BDCLCKID_SF=tRk8_KtKtCI3HnRY-P4_-tAt2qoXetJyaR3ma66bWJ5TMC_wDtJVBn5WX4Jn0lQzyTTR-RcgbKOKShPC-tn1DTk8MHrz2ljLtR6f-M5p3l02Vbc9e-t2yU_V34uHe4RMW23i0h7mWpI-VKF4D6tKejb3epJf-K68MIJ0WJk8Kb7Vbn530bbkbfJBD4QqQbvtaJvwKMbIQxcifqbTWbuVefI7yajK2MrRLgFfKDJGaC-MeCnb3UOpQT8ry4FOK5Oib4j7Lt3mab3vOpvTXpO1yjKreGKjtT0DJJkHV-35b5r5HJrTb4nKq4teheT22jnAJD3eaJ5nJD_BhRve3RKbXx-7bbozXnQR520tXpRvQpP-HJ7XefO2yRFDKq0LW4ny5mnPKl0MLpbtbb0xynoDbRDSKMnMBMni52OnapIKLIFKMDDxDjA2e5PShMntKI6J5Co20Rr2HJOoDDvnX535y4LdjGKfWftJaC8f2q3jWM5Ao-5eQlL-QptV3-Aq54REtDvl3Jjp5IP5D-89K4r6QfbQ0M6hqP-jW5Tasl3qyn7JOpvobUnxyMcB0aCDJ5kDtb-HVbOsa-5fKRopMtOhq4tehH4DXpOeWDTm_D_5bIKBJMD6XxJJhlLlWhoRLTQv5Guq-pPKKR7-jKJlBToDLp_Ay-5XKPjl3mkjbncyfn02OPKz0TKV544syPRiKMRnWgKqbIFhfIKKhKL6DjRhh4Fehmc22Pc22-oB0TrJabC3bJAmKU6qLT5XLfrWhjDqJ2ox0b3GyfnhsM-GW-oCjl0njxQyLJct05bnbb3CanRpjfowWMonDh8qbG7MJUntKD8D3hOO5hvvOn3O3M7zjlOhDNtDt60jfn3tWJTOaj6jDbTnMIT8bKCShUFsQj_J-2Q-5hOy3KOEMnrPjUIMeb0JBUobW6vmWncCbxP-anTThpFu-n5jHjoQDauO3J; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=2; H_PS_645EC=ef079T2KUFi1lEc%2F8R997AcN8vS6QHbqc6qVKvBbr25g5tgI9Ult3PLmf21c%2F9SnbNrF; sug=3; sugstore=1; ORIGIN=0; bdime=0; BD_HOME=0",
	"Host": "www.baidu.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",

}

with open("dict/baidu_server_ip_lists.txt","r") as w:
	baidu_ip_list = [i.strip("\n") for i in w.readlines() if i.strip("\n")]

z_domain_list = []

def link_urlparse(link):

	if "http://" not in link and  "https://" not in link:
		link = "http://"+link

	try:
		res = urlparse.urlparse(link)
	except Exception,e:
		print "[urlparse]"+str(e)
		domain = ""
	else:
		domain = res.netloc

	if ":" in domain:
		domain = domain.split(":")[0]

	return domain


def reuslt_number_page(search_keyword):
	''' 请求百度 '''

	page_judge = u'<span class="pc">10'

	try:
		url = "https://www.baidu.com"+search_keyword
		print url
		cur = requests.get(url=url,headers=headers,timeout=3)
	except Exception,e:
		print "[requests_baidu]"+str(e)
		return False
	else:
		body = cur.text
		if page_judge in body:
			return True
		else:
			return False

def request_baidu(search_keyword):
	''' 请求百度 '''

	try:
		ip = random.choice(baidu_ip_list)
		url = "http://"+ip+search_keyword
		cur = requests.get(url=url,headers=headers,timeout=3)
	except Exception,e:
		print "[requests_baidu]"+str(e)
		if ip in baidu_ip_list:
			baidu_ip_list.remove(ip) # 移除不能用的ip
		request_baidu(search_keyword) # 重新执行函数
	else:
		body = cur.text
		soup = BeautifulSoup(body,"html.parser")
		link_list = [i.text for i in soup.find_all('a',{"class":"c-showurl"})]
		return link_list

class search_domain(object):
	''' 搜索子域名 '''

	def __init__(self,domain):

		self.domain = domain
		self.p = pool.Pool(20)
		self.tasks = []
		self.sub_domain = []

	def run(self):
		print "[Info]start scan domain:%s" % self.domain
		if reuslt_number_page(search_keyword="/s?wd=site%3A{}".format(self.domain)):
			print "[Info]start first scan type......"
			with open("dict/baidu_search_keyword_lists.txt","r") as w:
				keyword_list = [i.strip("\n") for i in w.readlines()]
			for key in keyword_list:
				self.tasks.append(self.p.spawn(self.site_inurl_search, key))
			self.p.join()
			gevent.joinall(self.tasks)
		else:
			print u"baidu search number is low,so don't use first scan type......"

		print u"[Info]start second scan type......"
		self.site_link_search()
		print u"[Info]start third scan type......"
		self.site_search()

		self.sub_domain = list(set(self.sub_domain))

		return self.sub_domain

	def domain_(self,link_list,domain):
		''' 域名处理入库 '''

		for link in link_list:
			z_domain = link_urlparse(link)
			if z_domain not in z_domain_list and domain in z_domain:
				z_domain_list.append(z_domain)
				try:
					print z_domain
					self.sub_domain.append(z_domain)
				except:
					pass

	def site_link_search(self):
		# 第一种方式，site:baidu.com link:baidu.com

		for page in range(76):
			link_list = request_baidu(search_keyword="/s?wd=site%3A{}%20link:{}&pn={}&rn=50".format(self.domain,self.domain,page*10))
			if link_list:
				self.domain_(link_list,self.domain)
			else:
				break

	def site_inurl_search(self,key):
		# 第二种方式 site:baidu.com inurl:keyword

		link_list = request_baidu(search_keyword="/s?wd=site%3A{}%20inurl:{}&rn=50".format(self.domain,key))
		if link_list:
			self.domain_(link_list,self.domain)


	def site_search(self):
		# 第三种方式 site:baidu.com

		for page in range(76):
			link_list = request_baidu(search_keyword="/s?wd=site%3A{}&pn={}&rn=50".format(self.domain,page*10))
			if link_list:
				self.domain_(link_list,self.domain)
			else:
				break
		

if __name__=="__main__":

	import sys
	if len(sys.argv)>1:
		domain = sys.argv[1]
		cur =search_domain(domain)
		print cur.run()
	else:
		print "[Help] For Example: python domain_baidu_search.py target_domain"








			
