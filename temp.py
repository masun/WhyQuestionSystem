import re
import os
import time
import urllib2
import sys
import requests
import lxml.html as lh
from BeautifulSoup import UnicodeDammit

HEADERS = {'User-agent': 'Mozilla/5.0'}
inicio = time.time()
toDeleteRegex = re.compile(r'<body>\n[:]|<table.+?</table>|<style.+?</style>|<figure.*?</figure>|<normallist>.*?</normallist>|<conversionwarning>.*?</conversionwarning>|<languagelink.*?</languagelink>|<template.*?</template>|<indentation.*?</indentation.*?>|<script.+?</script>|From Wikipedia, the free encyclopedia',re.DOTALL)#|<emph3>|</emph3>|\n\s*[0-9]+\s*\n
tagRegex = re.compile(r'<.*?>',re.DOTALL)
toEnterRegex = re.compile(r'<p>|</p>|<name id=.+?>|</name>|<section>|<title>.*?</title>',re.DOTALL)#|<title>|</title>
spaceRegex = re.compile(r'\n+|\n \n')
lineaPalabraFinal = re.compile(r'(?![^A-Za-z])\n')
file_name_form = re.compile(r'/(.+?)\b',re.DOTALL)

def lhget(*args, **kwargs):
    r = requests.get(*args, **kwargs)
    html = UnicodeDammit(r.content).unicode
    tree = lh.fromstring(html)
    return tree

def remove(el):
    el.getparent().remove(el)


def transform_from_url(url,destiny):
	text = ""
	tree = lhget(url, headers=HEADERS)
	all_paragraph = tree.xpath("//div[@class='mw-content-ltr']/p")

	for el in all_paragraph:

		for ref in el.xpath("//sup[@class='reference']"):
		    remove(ref)

		#print lh.tostring(el, pretty_print=True)
		text += el.text_content() + "\n"
	return text


def transform(origin, destiny):
	f = open(origin)
	content = f.read()
	f.close()
	f = open(destiny,"w")
	f.write(xml_tag_cleaner(content))
	f.close()

def document_list(entry):
	doc_list = []
	if os.path.isdir(entry):
		if entry[len(entry)-1] != "/":
			entry += "/"
		sub_entries = os.listdir(entry)
		for sub_entry in sub_entries:
			new_entry = entry + sub_entry
			doc_list.extend(document_list(new_entry))
		return doc_list
	else:
		return [entry]


def xml_tag_cleaner(content):
	return re.sub(spaceRegex , "\n", re.sub(tagRegex, "", re.sub(toEnterRegex,"\n", re.sub("\n"," ", re.sub(toDeleteRegex,"",content)))))

if __name__ == "__main__":
	print
	print
	print
	print
	print
	print
	print
	print sys.argv[1]

	print transform_from_url(sys.argv[1],"destiny")







'''
eList = os.listdir("../Wikipedia/Wikipedia2006/2006XML/")[1:]
x = 0
for e in eList:
	iList = os.listdir("../Wikipedia/Wikipedia2006/2006XML/"+e)[1:]
	for i in iList:
		print str(x) + "vo		documento: " + i + ",		" + str(time.time()-inicio) + "		segundos."
		f = open("../Wikipedia/Wikipedia2006/2006XML/"+e+"/"+i)
		content = f.read()
		notagContent = re.sub(spaceRegex , "\n", re.sub(tagRegex, "", re.sub(toEnterRegex,"\n", re.sub("\n"," ", re.sub(toDeleteRegex,"",content)))))
		f.close()
		f = open("../Wikipedia/Wikipedia2006/2006TXT/"+e+"/"+i[:(len(i)-3)]+"txt",'w')
		f.write(notagContent)
		f.close()
		x = x + 1

final = time.time() - inicio
print "EL tiempo final " + str(final) + "segundos"
print "Fueron " + str(x) + " documentos"
'''