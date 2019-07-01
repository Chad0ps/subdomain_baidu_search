#! -*- coding:utf-8 -*-

__author__="nMask"
__Date__="1 Jul 2019"
__Blog__="https://thief.one"
__version__="1.0"
__py_version__="2.7.11"


from plugins.domain_baidu_search import search_domain
from plugins.brute_crack import brute_crack

def scan(domain):

	print "[domain]%s[plugins]%s........." % (domain,"search_domain")
	cur_search_domain = search_domain(domain)
	subdomain_list = cur_search_domain.run()
	print subdomain_list


	print "[domain]%s[plugins]%s........." % (domain,"brute_crack")
	cur_brute_crack = brute_crack(domain)
	subdomain_list = cur_brute_crack.run()
	print subdomain_list

if __name__=="__main__":
	
	scan("baidu.com")