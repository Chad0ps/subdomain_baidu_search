#! -*- coding:utf-8 -*-

__author__="nMask"
__Date__="1 Jul 2019"
__Blog__="https://thief.one"
__version__="1.0"
__py_version__="2.7.11"


import random
import dns.resolver
import gevent
from gevent import monkey, pool
monkey.patch_all()

try:
	with open("dict/dns_servers_lists.txt","r") as w:
		dns_server = [ i.strip("\n") for i in w.readlines()]
except:
	with open("../dict/dns_servers_lists.txt","r") as w:
		dns_server = [ i.strip("\n") for i in w.readlines()]
try:
    with open("dict/subdomain_keyword_lists.txt","r") as w:
        subdomain_keyword = [ i.strip("\n") for i in w.readlines()]
except:
    with open("../dict/subdomain_keyword_lists.txt","r") as w:
        subdomain_keyword = [ i.strip("\n") for i in w.readlines()]

def filter_ip(ip):

	ip_black = ["127.0.0.1","0.0.0.0","0.0.0.1"]

	try:
		ip_split = ip.split(".")
		ip_1 = ip_split[0]
		ip_2 = ip_split[0]+ip_split[1]

		if ip_1=="10" or ip_1=="172" or ip in ip_black:
			return False
		elif ip_2=="192168":
			return False
		else:
			return True
	except Exception,e:
		print "[filter_ip]%s" % e
		return False

class brute_crack(object):

	def __init__(self,domain):
		
		self.sub_domain_list = []
		self.domain_ip_num = {}
		self.domain = domain
		self.jobs = []
		

	def run(self):

		if not self.dns_request(sub_domain="nmaskistestdomain."+self.domain,num=0):
			p = pool.Pool(20)
			for num,keyword in enumerate(subdomain_keyword):
				sub_domain = keyword+"."+self.domain
				self.jobs.append(p.spawn(self.dns_request,sub_domain,num))
			p.join()
			gevent.joinall(self.jobs)

			return self.sub_domain_list
		else:
			return []

	def dns_request(self,sub_domain,num):
	 	
	 	try:
	 		dns_server_ = random.choice(dns_server)
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [dns_server_]
			ip = str(my_resolver.query(sub_domain,"A")[0])
			if filter_ip(ip):
				print "[num]%s[dns]%s[domain]%s[ip]%s" % (num,dns_server_,sub_domain,ip)
				self.sub_domain_list.append(sub_domain)
				return True
		except:
			pass

if __name__=="__main__":

	cur = brute_crack("airbnbcitizen.com")
	print cur.run()



