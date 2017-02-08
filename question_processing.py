import optparse
import re
import os
from lemmatizadorWordnet import lemmatizar_documento

''' Entra la pregunta, 
	guardarla en un documento
	***la convierto en una lista de palabras
	la lemmatizo 
	la convierto en un vector TF_IDF
	la introduzco dentro de la matriz de pesos
'''

def question_preprocessing(question, container_folder):
	f = open(container_folder + 'temp.txt','w')
	f.write(question)
	f.close()
	lemmatizar_documento(container_folder + 'temp.txt',container_folder + 'question.txt')
	return container_folder + 'question.txt'
	


if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-q', help='pregunta a realizar (entre comillas)', default="why is the sky blue", type='string', dest='question')
	parser.add_option('-d', help='documento a crear para el resultado de la lemmatizacion', type='string', dest='directory')
	parser.add_option('-t', help='documento para escribir la pregunta', type='string', dest='temporal')

	
	(opts, args) = parser.parse_args()
	mandatories = ['directory', 'temporal']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)
	question_processing(opts.question,opts.temporal,opts.directory)