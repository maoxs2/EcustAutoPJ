import requests
from lxml import etree
import mechanize
import urllib2
import sys

def pj_ty(href):
	response = br.open(href)
	br.select_form(name="Form1")
	i=1
	for i in xrange(1,5):
		br["yq" + str(i)] = ["25"]
	br["yq17"] = ["100"]
	br.submit()
	print "OK"

def pj_bds(href):
	response = br.open(href)
	br.select_form(name="Form1")
	html = response.read()
	HTML_filter = etree.HTML(html)
	for i in xrange(1,20):
		values = HTML_filter.xpath("//input[@name='yq"+str(i)+"']")
		z = 1
		for value in values:
			if z == 1 :
				br.form["yq" + str(i)] = [values[0].attrib['value']]
			else:
				break
	br.submit()
	print "OK"

def pj_normal(href):
	response = br.open(href)
	br.select_form(name="Form1")
	html = response.read()
	HTML_filter = etree.HTML(html)
	i =1
	for i in xrange(1,20):
		values = HTML_filter.xpath("//input[@name='yq"+str(i)+"']")
		z = 1
		for value in values:
			if z == 1 :
				br.form["yq" + str(i)] = [values[0].attrib['value']]
			else:
				break
	br.submit()
	print "OK"
			
br = mechanize.Browser()
s = requests.Session()

user_info = sys.argv[1].split("x")
user_id = user_info[0]
user_pw = user_info[1]

#options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

login_url = "http://pjb.ecust.edu.cn/pingce/login.php"
p = s.post(login_url, {'action':"login", 'sno':user_id,'password':user_pw})
txt1 = p.text
o = s.get("http://pjb.ecust.edu.cn/pingce/list.php")
txt2 = o.text
o.encoding = "gbk"
txt = o.text.encode("gbk")

if txt1 != txt2 :
	exit()

html = etree.HTML(txt)
hrefs = html.xpath("//tr[@class='row']/td[@class='subject']/a")

cookie = s.cookies
br.set_cookiejar(cookie)
for href in hrefs:
	pj_href = "http://pjb.ecust.edu.cn/pingce/" + href.attrib['href']
	print pj_href
	print pj_href.find("typg")

	if  pj_href.find("typg") > 0 :
		pj_ty(pj_href)
	elif  pj_href.find("bdspg.php") > 0:
		pj_bds(pj_href)
	else:
		pj_normal(pj_href)

print 'Successful'