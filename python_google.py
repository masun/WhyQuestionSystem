import urllib2
import re
from sets import Set
snipped_form = re.compile(r'<h3 class="r"><a href=\"/url\?q=(http://en\.wikipedia\.org.*?)&amp;.*?<span class="st">(.*?)</span>', re.DOTALL)
#.*?<span class="st">(.*?)</span>
headers = {'User-agent':'Mozilla/11.0'}

def get_google_url(search,number_pages=0, siteurl=False):
    if siteurl==False:
        return ['http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)+ '&start=' + str(x) + '0' for x in range(number_pages)]
        
    else:
        return ['http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+'&oq=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+ '&start=' + str(x) + '0' for x in range(number_pages)]

def get_google_links(search,number_pages=2,siteurl=False):
   #google returns 403 without user agent
   url_list = get_google_url(search,number_pages,siteurl)
   links =[]
   #wikipedia_link_form = re.compile(r'http://en.wikipedia.org/.*?#')

   c = []
   for url in url_list:

	   req = urllib2.Request(url,None,headers)
	   site = urllib2.urlopen(req)
	   data = site.read()
	   site.close()
	   #print url
	   #print data
	   #exit(-1)
	   c.extend(re.findall(snipped_form,data))
   for x in range(len(c)):
	   	snip = str(c[x][1])
	   	snip = re.sub(r'<.+?>',"",snip)
	   	snip = re.sub(r' +'," ",snip)
	   	snip = re.sub('&nbsp',"",snip)	
	   	c[x] =  (re.sub('%25','%',c[x][0]),snip)
   return c


def get_google_from_one_link(url):
	req = urllib2.Request(url,None,headers)
	site = urllib2.urlopen(req)
	data = site.read()
	site.close()
	#print url
	#print data
	#exit(-1)
	c = re.findall(snipped_form,data)
	
	for x in range(len(c)):
	   	snip = str(c[x][1])
	   	snip = re.sub(r'<.+?>',"",snip)
	   	snip = re.sub(r' +'," ",snip)
	   	snip = re.sub('&nbsp',"",snip)
	   	c[x] =  (re.sub('%25','%',c[x][0]),snip)
	return c


if __name__ == "__main__":
	lista = get_google_links('why is the sky blue',9,'http://en.wikipedia.org')
	print len(lista)
	exit(-1)
	for l in lista:
		print l
		print 
	