# Herramienta para el Sistema de Busqueda de Respuestas: Lemmatizador en WordNet
# Creado por: Charles Ochoa 
"""
Este programa tiene la funcion de reducir la cantidad de palabras derivadas a un mismo significado
este programa se usa por la linea de comando. Recibe 2 entradas: la primera es el directorio de entrada,
que contienen a su vez las carpetas que con los los documentos adentro. la segunda entrada es el directorio 
destino, en donde se va a replicar el mismo patron encontrada en el directorio de entrada, y se crearan
los documentos con la lista de palabras reducidas de cada documento.

Modificaciones pendientes:
	- modificaciones de prefijos a prefijos comunes y buscar prefijos relacionados con topicos de tecnologia
	- Igual con los sufijos.
	- Buscar nombres de empresas, nombres de personas, paises


Uso:
python lemmatizadorWordnet.py Directorio/de/Entrada/ Directorio/de/Salida/

"""	


# Reducir la lista a common prefix and suffix
#
import time
import re
import sys
import os
import subprocess
import aspell
import nltk
import pprint
import thread
from nltk.corpus import wordnet as wn 
from nltk.corpus import names
from nltk.stem.wordnet import WordNetLemmatizer
from sets import Set

#Preparando el ambiente
os.system("export PATH=/Users/warles34/Documents/Research/CODE/Tesis/stanford-ner-2012-11-11/stanford-ner.jar:$PATH")
lemmatizer = WordNetLemmatizer()
wordForm = re.compile(r"\b[A-Za-z]+\b")
diccionario = aspell.Speller('lang','en')
s1 = open("stopwords.txt","r")
stopwords = Set(re.findall(wordForm, s1.read()))
entidadform=re.compile(r'([A-Za-z.]+)/[A-Za-z][A-Za-z]+[ ]+')
entidadORGA = re.compile(r'(([A-Za-z]+)/ORGANIZATION[ ]+)+')
entidadMISC = re.compile(r'(([A-Za-z]+)/MISC[ ]+)+')
entidadLOCA = re.compile(r'(([A-Za-z]+)/LOCATION[ ]+)+') 
entidadPERS = re.compile(r'(([A-Za-z]+)/PERSON[ ]+)+')
no_entidadform=re.compile(r'([A-Za-z]+)/O ')
#borre micro de esta lista por la existencia de Microsoft
listaPreffix = Set(['a', 'an', 'ante', 'anti', 'auto', 'circum', 'co', 'com', 'con', 'contra', 'de', 'dis', 'en', 'ex', 'extra', 'hetero', 'homo', 'hyper', 'il', 'im', 'in', 'ir', 'in', 'inter', 'intra', 'macro', 'mono', 'non', 'omni', 'post', 'pre', 'pro', 'sub', 'syn', 'trans', 'tri', 'un', 'uni'])
#listaALotPreffix = ['a', 'ab', 'abs', 'ac', 'acet', 'aceto', 'acr', 'acro', 'actin', 'actino', 'ad', 'aden', 'adeno', 'ae', 'aer', 'aero', 'af', 'afro', 'after', 'ag', 'agr', 'agri', 'agro', 'al', 'allo', 'ambi', 'amphi', 'an', 'ana', 'and', 'andr', 'andro', 'anemo', 'angio', 'anglo', 'ano', 'antho', 'anthrop', 'anthropo', 'ante', 'ant', 'anth', 'anti', 'ap', 'apo', 'aqua', 'aque', 'aqui', 'arc', 'arch', 'archi', 'archaeo', 'archeo', 'aristo', 'arithmo', 'arterio', 'arthr', 'arthro', 'astr', 'astro', 'at', 'atto', 'audio', 'aut', 'auto', 'azo', 'bacter', 'bacteri', 'bacterio', 'bar', 'baro', 'bathy', 'be', 'benz', 'benzo', 'bi', 'bin', 'biblio', 'bio', 'blast', 'blasto', 'brachy', 'brady', 'brom', 'bromo', 'bronch', 'bronchi', 'broncho', 'bry', 'bryo', 'by', 'bye', 'caco', 'carb', 'carbo', 'cardi', 'cardio', 'cel', 'celo', 'cen', 'ceno', 'cent', 'centi', 'centr', 'centri', 'cephal', 'cephalo', 'chalco', 'cheiro', 'chem', 'chemi', 'chemico', 'chemo', 'chino', 'chiro', 'chlor', 'chloro', 'choan', 'choano', 'chol', 'chole', 'christo', 'chron', 'chrono', 'chrys', 'chryso', 'cine', 'circum', 'cis', 'co', 'coel', 'coelo', 'coen', 'coeno', 'col', 'com', 'copr', 'copro', 'con', 'contra', 'cor', 'cosmo', 'counter', 'cryo', 'crypto', 'cyan', 'cyano', 'cyber', 'cycl', 'cyclo', 'cyn', 'cyno', 'cyt', 'cyto', 'de', 'dec', 'deca', 'deci', 'deka', 'demi', 'deoxy', 'deuter', 'deutero', 'di', 'dia', 'di', 'dichlor', 'dichloro', 'dinitro', 'dino', 'dipl', 'diplo', 'dis', 'di', 'dodec', 'dodeca', 'down', 'dys', 'eco', 'ecto', 'eigen', 'electr', 'electro', 'em', 'en', 'end', 'endo', 'ennea', 'ent', 'ento', 'epi', 'equi', 'ethno', 'eu', 'eur', 'euro', 'ever', 'ex', 'exa', 'exbi', 'exo', 'extra', 'femto', 'ferro', 'fluor', 'fluori', 'fluoro', 'for', 'fore', 'forth', 'franco', 'full', 'ful', 'gain', 'gastr', 'gastro', 'genito', 'geo', 'gibi', 'giga', 'gen', 'geno', 'gymno', 'gyn', 'gyno', 'gyro', 'haem', 'haemat', 'haemo', 'hagi', 'hagio', 'half', 'hect', 'hecto', 'heli', 'helio', 'hem', 'hemat', 'hemi', 'hemo', 'hendeca', 'hept', 'hepta', 'hetero', 'hex', 'hexa', 'hind', 'hinder', 'hipp', 'hippo', 'hispano', 'hist', 'histio', 'histo', 'hol', 'holo', 'homeo', 'homo', 'homoeo', 'hydro', 'hyper', 'hypn', 'hypno', 'hypo', 'il', 'ill', 'im', 'in', 'ind', 'indo', 'indo', 'inter', 'intra', 'ir', 'is', 'iso', 'italo', 'ker', 'kibi', 'kilo', 'kuli', 'like', 'lip', 'lipo', 'lith', 'litho', 'macr', 'macro', 'mal', 'many', 'mani', 'mebi', 'mega', 'mes', 'meso', 'meta', 'metro', 'micro', 'mid', 'midi', 'milli', 'mini', 'mis', 'miso', 'mon', 'mono', 'multi', 'myria', 'myxo', 'nano', 'naso', 'necr', 'necro', 'neo', 'non', 'non', 'nona', 'oct', 'octa', 'octo', 'off', 'olig', 'oligo', 'omni', 'on', 'orth', 'ortho', 'other', 'out', 'over', 'ov', 'ovi', 'ovo', 'palaeo', 'pale', 'paleo', 'par', 'para', 'pebi', 'pent', 'penta', 'peta', 'phon', 'phono', 'photo', 'phys', 'physi', 'physio', 'pico', 'post', 'poly', 'praeter', 'pre', 'preter', 'prot', 'proto', 'pseud', 'pseudo', 'psych', 'psycho', 'pter', 'ptero', 'pyro', 'quadr', 'quadri', 'quadru', 'quarter', 'quasi', 'quin', 'quinqu', 'quinque', 'radi', 'radio', 're', 'robo', 'ribo', 'same', 'schiz', 'schizo', 'self', 'semi', 'sept', 'septa', 'septem', 'septi', 'sex', 'sexa', 'sino', 'step', 'sub', 'sui', 'super', 'supra', 'syl', 'sym', 'syn', 'tebi', 'tele', 'ter', 'tera', 'tetr', 'tetra', 'therm', 'thermo', 'thorough', 'to', 'trans', 'tri', 'twi', 'ultra', 'um', 'umbe', 'un', 'under', 'uni', 'up', 'ur', 'uro', 'vice', 'wan', 'well', 'wiki', 'with', 'xeno', 'xero', 'xylo', 'y', 'yocto', 'yotta', 'zepto', 'zetta', 'zo', 'zoo']

  
english_names = set([name for filename in ('male.txt', 'female.txt') for name
             in names.words(filename)])
  


NounSuffixes = Set(['acy', 'al', 'ance', 'ence', 'dom', 'er', 'or', 'ism', 'ist', 'ity', 'ty', 'ment', 'ness', 'ship', 'sion', 'tion'])
VerbSuffixes = Set(['ate', 'en', 'ify', 'fy', 'ize', 'ise'])
AdjectiveSuffixes = Set(['able', 'ible', 'al', 'esque', 'ful', 'ic', 'ical', 'ious', 'ous', 'ish', 'ive', 'less', 'y'])
listaSuffix = NounSuffixes | VerbSuffixes | AdjectiveSuffixes
#listaSuffix = ['able', 'ably', 'ad', 'ade', 'age', 'agogy', 'al', 'ality', 'al', 'ality', 'al', 'ity', 'an', 'an', 'ance', 'ancy', 'ant', 'ant', 'ar', 'ar', 'ard', 'ary', 'ary', 'arch', 'archy', 'ate', 'ate', 'ate', 'athlon', 'ation', 'ation', 'ate', 'ative', 'atory', 'bound', 'cele', 'coele', 'coel', 'cele', 'centesis', 'cephalic', 'chondrion', 'cide', 'city', 'cy', 'cycle', 'dom', 'ectasia', 'ectasis', 'ectomy', 'ed', 'ee', 'eer', 'eme', 'emia', 'en', 'en', 'enchyma', 'ence', 'ency', 'ent', 'ent', 'eous', 'er', 'or', 'ergy', 'ern', 'ery', 'ese', 'esque', 'ess', 'esthesis', 'esthesia', 'etic', 'ette', 'fare', 'ful', 'gate', 'gnosis', 'gon', 'gry', 'hedron', 'holic', 'hood', 'ia', 'iable', 'ial', 'ian', 'ian', 'ian', 'iant', 'iary', 'iate', 'ible', 'able', 'ibly', 'ic', 'ical', 'ics', 'id', 'al', 'iency', 'ient', 'ier', 'ile', 'illion', 'ious', 'ing', 'ing', 'ion', 'ish', 'ish', 'ism', 'ist', 'ista', 'ite', 'itis', 'itive', 'itude', 'ity', 'ium', 'ive', 'ization', 'isation', 'ize', 'ise', 'izzle', 'kinesis', 'less', 'let', 'like', 'ling', 'ly', 'like', 'ly', 'like', 'man', 'mancy', 'mania', 'ment', 'meter', 'metry', 'mony', 'morphism', 'most', 'ness', 'nik', 'er', 'ocracy', 'ogram', 'ography', 'oid', 'oid', 'ologist', 'ology', 'ome', 'omics', 'omics', 'onomy', 'onym', 'opsy', 'or', 'er', 'or', 'our', 'ory', 'ory', 'ose', 'osis', 'ous', 'phagy', 'phagia', 'philia', 'phobia', 'phone', 'phyte', 'polis', 'science', 'scope', 'script', 'ship', 'sion', 'some', 'stan', 'ster', 't', 'th', 'eth', 'th', 'tion', 'tom', 'tome', 'tropism', 'ty', 'uary', 'ulent', 'uous', 'ure', 'us', 'ville', 'vore', 'vorous', 'ward', 'wards', 'ware', 'ways', 'wise', 'wright', 'y']

def NER_separation(direccion):

	os.system('export CLASSPATH="${CLASSPATH}:/Users/warles34/Documents/Research/CODE/Tesis/stanford-ner-2012-11-11/stanford-ner.jar"')
	#os.system("echo Charles")
	#os.system("echo $PATH")
	#os.system("echo $CLASSPATH")
	comando="java -mx600m edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ../stanford-ner-2012-11-11/classifiers/english.conll.4class.distsim.crf.ser.gz -textFile "+direccion
	#print comando
	doc=subprocess.check_output(["java", "-mx600m", "edu.stanford.nlp.ie.crf.CRFClassifier", "-loadClassifier", "../stanford-ner-2012-11-11/classifiers/english.conll.4class.distsim.crf.ser.gz", "-textFile", direccion])
	return doc

def entity_noentity_extraction(doc):
	entidad=re.findall(entidadform,doc)
	entidad = [w.lower() for w in entidad]
	no_entidad=re.findall(no_entidadform,doc)
	no_entidad = root(no_entidad)
	return (entidad,no_entidad)
	

def quitarPrefijo(word,l):
	nueva = []
	for prefijo in listaPreffix:
		if word[:len(prefijo)] == prefijo and len(word) - len(prefijo) > 2:
			nuevaWord = word[len(prefijo):]
			if diccionario.check(nuevaWord) or wn.synsets(nuevaWord) != []:
				#print word + ", su PRE APROBADO: " + nuevaWord + "		En documento: " + l
				nueva.append(nuevaWord)
	#print nueva
	return nueva
	
	
def quitarSufijo(word,l):
	nueva = []
	for sufijo in listaSuffix:
		if word[len(sufijo):] == sufijo and len(word) - len(sufijo) > 2:
			nuevaWord = word[:len(sufijo)]
			if diccionario.check(nuevaWord) or wn.synsets(nuevaWord) != []:
				#print word + ", su SUF APROBADO: " + nuevaWord + "		En documento: " + l
				nueva.append(nuevaWord)

	#print nueva
	return nueva


def root(old_lista,l=""):
	lista = []
	nuevapre = []
	nuevasu = []
	new_lista = []
	lemma_wordnet = []
	for w in range(len(old_lista)):
		word = str(str(old_lista[w]).lower())
		lista.append(word)
	for word in lista:
		if word in stopwords:
			#print "Es un STOPWORD: " + word
			pass
		elif wn.synsets(word) == []:
			#print "No esta en WordNet: " + word
			#print "  Se procede a quitar sufijo y prefijo..."
			word_sin = quitarSufijo(word,l)
			word_sin.append(quitarPrefijo(word,l))
			#print "  Tenemos las siguientes nuevas palabras:"
			#print "  " + str(word_sin)
			max_len = 2
			res_word = ""
			for sin in word_sin:
				if max_len != max(len(sin), max_len):
					res_word = sin
			if len(res_word) > 2:
				#print "Se agrega la palabra: " + res_word
				new_lista.append(word)
		elif wn.synsets(word) != []:
			#print "Se encuentra en WordNet: " + word
			new_lista.append(lemmatizar(word))
	return new_lista




	#print new_lista


def lemmatizar(elem):
	#print "Se va a lemmatizar: " + elem
	syn = wn.synsets(elem)
	if syn != []:
		if syn[0].pos == wn.VERB:
			elem = lemmatizer.lemmatize(elem,'v')
		elif syn[0].pos == wn.NOUN:
			elem = lemmatizer.lemmatize(elem,'n')
		elif syn[0].pos == wn.ADJ:
			elem = lemmatizer.lemmatize(elem,'a')
	return elem


def lemmatizar_documento(i,o):
	print o 
	doc = NER_separation(i)
	(e,ne) = entity_noentity_extraction(doc)
	e.extend(root(ne))
	docSalida = open(o,'w')
	for elem in e:
		docSalida.write(elem)
		docSalida.write("\n")	
	docSalida.close()


def lemmatizar_varios_documentos(i_list, o_list):
	all_doc = ""
	division = "\n\n-----------------------------------------------------------------------------------------\n\n"
	document_unit_form = re.compile(r'(.*?)-----------------------------------------------------------------------------------------',re.DOTALL)
	for elem in i_list:
		f = open(elem)
		content = f.read()
		f.close()
		all_doc += content + division
	f = open('temp.txt','w')
	f.write(all_doc)
	f.close()
	doc = NER_separation('temp.txt')
	print 
	print 
	print 
	print 
	print 
	print 
	print 
	print 
	all_ =  re.findall(document_unit_form,doc)
	for elem in range(len(all_)):
		(e,ne) = entity_noentity_extraction(all_[elem])
		e.extend(root(ne))
		f = open(o_list[elem],'w')
		for word in e:
			f.write(word+"\n")
		f.close()


#python lemmatizadorWordnet.py ../Wikipedia/Wikipedia2006/2006TXT/part-120000/250240.txt

if __name__ == '__main__':
	total_doc = 670000.0
	present_doc = 0.0
	tiempo = time.time()
	listFiles = os.listdir(sys.argv[1])[4:]
	for l in listFiles:
		bigs = len(listFiles)
		try:
			os.mkdir(sys.argv[2]+l)
		except:
			pass
		cs = os.listdir(sys.argv[1]+l)[1:]
		s = len(cs)
		for c in cs:
			print "La evaluacion lleva un " + str(present_doc*100.0/total_doc) + "% de ejecucion"
			present_doc+=1
			i = sys.argv[1]+l+"/"+c
			o = sys.argv[2]+l+"/"+c
			if not os.path.isfile(o):
				print o 
				(e,ne) = entity_noentity_extraction(NER_separation(i))
				e.extend(root(ne))
				docSalida = open(o,'w')
				for elem in e:
					docSalida.write(elem)
					docSalida.write("\n")
				exit(-1)
				print "Tiempo hasta el momento"
				print "									" + str(time.time())

	tiempo = time.time() - tiempo 
	print "El tiempo final fue"
	print tiempo
			
			
	