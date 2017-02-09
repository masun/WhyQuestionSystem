from multiprocessing import Pool
import re
import urllib
import socket 
# timeout in seconds 
timeout = 15
socket.setdefaulttimeout(timeout) 

	

sourcePage = 'http://wiki.answers.com/Q/'
whyAnswer = re.compile(r'<div id="editorText">[, \w]*</div>')
numberOfQuestions = range(1,16)
f = open('AnswersToWhyQuestions.txt', 'w')
fQuest = open('AllWhyWith_Separation.txt' , 'r+')



def getAnswer(question):
	print "hola"
	try :
		print question
		url = sourcePage + question
		webpage = urllib.urlopen(url)
		page = webpage.read()
		webpage.close()
	except IOError :
		page = ["Page fail"]
	retrievedAnswers = whyAnswer.findall(page)
	for x in retrievedAnswers :
		print x
		f.write(x)
		f.write('\n')
	if not retrievedAnswers :
		f.write("No answer\n")
	return "te amo proceso"
	


if __name__ == '__main__':
	pool = Pool(processes=16)
	for x in numberOfQuestions :
		porcentage = (x/16)*100
		print 'Process already done: ' +  str(porcentage) + '%'
		question = fQuest.readline()
		p = pool.apply_async(getAnswer,question)
		print(p.get(timeout=1)) 
		print "termino"

		

	f.close()
	fQuest.close()
