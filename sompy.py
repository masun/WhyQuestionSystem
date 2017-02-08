from __future__ import division

## Kyle Dickerson
## kyle.dickerson@gmail.com
## Jan 15, 2008
##
## Self-organizing map using scipy
## This code is licensed and released under the GNU GPL

## This code uses a square grid rather than hexagonal grid, as scipy allows for fast square grid computation.
## I designed sompy for speed, so attempting to read the code may not be very intuitive.
## If you're trying to learn how SOMs work, I would suggest starting with Paras Chopras SOMPython code:
##  http://www.paraschopra.com/sourcecode/SOM/index.php
## It has a more intuitive structure for those unfamiliar with scipy, however it is much slower.

## If you do use this code for something, please let me know, I'd like to know if has been useful to anyone.

from random import *
from math import *
import sys
import scipy

def min_max_range_matrix(matrix):
    l = 1000
    b = -1000
    for doc in matrix:
        l = min(min(doc),l)
        b = max(max(doc),b)

    return (l,b)


class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[ [random() for i in range(FV_size)] for x in range(width)] for y in range(height)])


    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, iterations=1000, train_vector=[[]], epsilon=0.001):
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        i = 0
        old = delta_nodes
        while i <= iterations:
            print self.difference(old) > epsilon
            print self.difference(delta_nodes)
            print i <= iterations
            i+=1
            st = "[["
            for x in range(self.height):
                for y in range(self.width):
                    for e in range(self.FV_size):
                        st+=str(int(self.nodes[x,y,e]))+" "
                    st+= "] , ["
                st+="]]\n\n"
            delta_nodes.fill(0)
            radius_decaying=self.radius*exp(-1.0*i/time_constant)
            #from PIL import Image
            #print "\nSaving Image: sompy_test_colors.png..."
            #img = Image.new("RGB", (self.width, self.height))
            #for r in range(self.height):
            #    for c in range(self.width):
            #        img.putpixel((c,r), (int(self.nodes[r,c,0]*255), int(self.nodes[r,c,1]*255 ), int(self.nodes[r,c,2]*255)))
            #img = img.resize((self.width*10, self.height*10),Image.NEAREST)
            #img.save("Test Colors/Test1/4_sompy_test_colors"+str(10000+i)+".png")
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying=self.learning_rate*exp(-1.0*i/time_constant)

            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations)+"\n")
            
            for j in range(len(train_vector)):
                #print train_vector 
                best = self.best_match(train_vector[j])
                for loc in self.find_neighborhood(best, radius_decaying):

                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    #sys.stdout.write("Influence: " + "/" + str(influence) + "\n")
                    inf_lrd = influence*learning_rate_decaying
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
            old = self.nodes
            self.nodes += delta_nodes
        sys.stdout.write("\n")
    
    # Returns a list of points which live within 'dist' of 'pt'
    # Uses the Chessboard distance
    # pt is (row, column)
    def find_neighborhood(self, pt, dist):
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors
    
    # Returns location of best match, uses Euclidean distance
    # target_FV is a scipy array
    def best_match(self, target_FV):
        loc = scipy.argmin((((self.nodes - target_FV)**2).max(axis=2))**0.5)
        r = 0
        while loc > self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)


    # Queda pendiente la distancia angular por el coseno de los vectores
    def best_match_cosine(self, target_FV):
        loc = scipy.argmin(self.nodes * target_FV).sum(axis=2)  


    def similarity_measure_cosine(self):
        max_sim_number = -1000
        max_document_index = -1
        disordered_list = []
        for j in range(len(self.TF_IDF_matrix[:-1])):
            sum_wq_wj = float(sum([a*b for a,b in zip(self.TF_IDF_matrix[j],self.question_TF_IDF_vector)]))
            sum_wq_2 = float(sum([a**2 for a in self.question_TF_IDF_vector]))
            sum_wj_2 = float(sum([a**2 for a in self.TF_IDF_matrix[j]]))
            jacard_sim_ = sum_wq_wj / (sum_wq_2 * sum_wj_2)**.5
            disordered_list.append((j,self.document_list[j],jacard_sim_))
            if jacard_sim_ > max_sim_number:
                max_sim_number = jacard_sim_
                max_document_index = j
        print "El documento con mayor Cosine similitud es: " + self.document_list[max_document_index]
        print "Con un valor de similitud de: " + str(max_sim_number)
        self.most_similar_document_indexes = sorted(disordered_list, key= lambda similarity: similarity[2],reverse=True)


    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5

    def difference(self, delta_nodes):
        #print self.nodes
        #print delta_nodes
        delta = 0
        for x in range(len(self.nodes)):
            delta =+ sum(abs(self.nodes[x] - delta_nodes[x]))
        #print delta
        return sum(delta)

if __name__ == "__main__":
    print "Initialization..."
    colors = [[0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    width = 32
    height = 32
    color_som = SOM(colors,width,height,3,5)
    print "Training colors..."
    color_som.train(100, colors)





        