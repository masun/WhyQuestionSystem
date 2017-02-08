import re
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from time import sleep

def divide_sentences(sentence):
	sentence_form = re.compile(r'[A-Z].*?\.+')
	return re.findall(sentence_form,sentence)

def extract_paragraph_from_snipp(file_,snipp):
	snipps = divide_sentences(snipp)
	result = ""
	counter = 0
	paragraph = ""
	f = open(file_)
	elem = 0
	ret = []
	for line in f:
		paragraph = word_tokenize(line)
		for s in snipps:
			words = word_tokenize(s)

			for w in words:
				if w in paragraph:
					counter += 1
			percentage = float(counter) / float(len(words))
			counter = 0
			if percentage > 0.8:
				new_name = file_[:len(file_)-4]+"-"+str(elem)+".txt"
				#print new_name
				f = open(new_name,'w')
				#print line
				f.write(line)
				f.close()
				ret.append(new_name)
				elem += 1
				break
	f.close()
	return ret
	

def main():
	extract_paragraph_from_snipp("obtencionPruebas/TXT/200001.txt","The sunlit sky is blue because air scatters short-wavelength light more than longer wavelengths. Since blue light is at the short wavelength end of the visible ...")

if __name__ == '__main__':
	main()