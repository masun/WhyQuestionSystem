import matplotlib.pyplot as plt 
from matrix_builder import WeightedMatrix
import numpy
from scipy import array
from collections import Counter
#Pruebas que hacer:
# 	Ver la distribucion de valores en la matriz de pesos
# 	Ver la distribucion de los valores que toman los pesos de la matriz
# 	Ver en que parte de la red neuronal caen los documentos, y su distribucion
#	Ver en que cluster caen la pregunta respecto a los candidatos a respuesta
#	



class Results:

	def __init__(self):
		self.weights = []
		self.number_distinct_words = 0 				#integer
		self.number_total_words = 0 				#integer
		self.number_of_words_in_document = []		#list of integer (size: number of documents)
		self.document_list = []						#list of strings (size: number of documents)
		self.word_total_frequency = []				#list of integer (size: number of distinct words)
		self.word_list = []							#list of strings (size: number of distinct words)
		self.document_frequency = []				#list of integer (size: number of distinct words)
		self.TF_IDF_matrix = []						#list of list of floats (size: number of documents x number of words)
		self.word_frequency_matrix = []				#list of list of integer (size: number of documents x number of words)
		self.question_frequency_vector = []			#list of floats (size: number of distinct words)
		self.question_TF_IDF_vector = []			#list of floats (size: number of distinct words)
		self.SOM_cluster 							#one SOM object




def plot_words_distribution(w_matrix,destiny):
	min_ = 10000
	matrix = w_matrix.word_frequency_matrix
	axis_y = len(matrix)

	axis_x = len(matrix[0])
	coor_x = []
	coor_y = []
	for y in range(axis_y):
		for x in range(axis_x):
			if matrix[y][x]:
				coor_y.append(y)
				coor_x.append(x)
	plt.plot(coor_x,coor_y,'ro')
	plt.ylabel('Documents')
	plt.xlabel('Words')
	plt.axis([-1, axis_x + 1, -1, axis_y + 1])
	plt.show(destiny+"words_distribution.jpg")
	return [coor_x,coor_y]

def plot_weight_distribution(w_matrix,destiny):
	matrix = w_matrix.word_frequency_matrix
	axis_y = len(matrix)
	axis_x = len(matrix[0])
	elements_not_min = []
	for y in range(axis_y):
		for x in range(axis_x):
			if matrix[y][x]:
				elements_non_zero.append(matrix[y][x])
	plt.hist(elements_non_zero)
	plt.ylabel('number of words')
	plt.xlabel('TF_IDF score')
	plt.show(destiny+"weight_distribution.jpg")

def documents_location_in_Map(cluster_network,matrix,destiny):
	coor_y = []
	coor_x = []
	clusters = []
	for row in range(len(matrix)):
		(x,y) = cluster_network.best_match(array(matrix[row]))
		clusters.append((x,y))
		coor_y.append(y)
		coor_x.append(x)
	plt.plot(coor_x,coor_y,'ro')
	plt.axis([-1,int(cluster_network.width)+1,-1,int(cluster_network.height)+1])
	plt.show(destiny+"location_in_Map.jpg")
	return Counter(clusters)

def percentage_documents_in_cluster(cluster_network,matrix):
	c = Counter()
	list_ = []
	
	for row in range(2,len(matrix)):
		print row
		(x,y) = cluster_network.best_match(array(matrix[row]))
		c[(x,y)]+=1
		list_.append([matrix[1][row-2],x,y])
	#exit(-1)



def location_of_question_in_map(w_matrix,destiny):

	coor_y = []
	coor_x = []
	clusters = []
	if  w_matrix.question_TF_IDF_vector == []:
		print "ERROR, Vector TF_IDF de pregunta aun no creado."
	else:
		cluster_network = w_matrix.SOM_cluster
		matrix = w_matrix.TF_IDF_matrix[:-1] ######### duda 
		for row in range(len(matrix)):
			(x,y) = cluster_network.best_match(array(matrix[row]))
			clusters.append((x,y))
			coor_y.append(y)
			coor_x.append(x)
		(x,y) = cluster_network.best_match(array(w_matrix.question_TF_IDF_vector))
		plt.plot(coor_x,coor_y,'b+')
		print "plt.plot([x],[y]): " + str(x) + " , " + str(y)
		print

		plt.plot(x,y,'rx')
		plt.axis([-1,int(cluster_network.width)+1,-1,int(cluster_network.height)+1])
		plt.show(destiny+"location_in_Map.jpg")
	return clusters



if __name__ == '__main__':
	matrix = [[1,2,3,4],[5,6,1,8],[10,11,12,1]]
	plot_weight_distribution(matrix)