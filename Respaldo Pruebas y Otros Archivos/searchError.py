import os 
import re
import MySQLdb
import sys
from sets import Set
db=MySQLdb.connect(db= "wikipedia", passwd= "19335350Garfield", user="ochoaC")
cur = db.cursor()

pair = re.compile("([a-z0-9]+)\|(.+?)(?=\n|\Z)")
inputFolder = "../DBdocuments/WordDocument/"
listFiles = os.listdir(inputFolder)
s = 1203.0
count = 0.0
arch = open("ErrorFolder.txt", 'a')
for name in listFiles[1:]:
	count = count + 1.0
	f = open(inputFolder + name,'r')
	doc = f.read()
	f.close()
	elements = pair.findall(doc)
	insList = [x[1] for x in elements]
	howMany = insList.count("Error")
	if howMany > 0:
		arch.write("Aparecio un ERROR in:  " + name + "\n")	
	sys.stdout.write("\r" +name + ": processing.. ")
	sys.stdout.flush()
	por = count*100 / s
	sys.stdout.write("\r" +name + ": processing..      and total: " + str(por)[:7] + "%")
	sys.stdout.flush()
      

      

