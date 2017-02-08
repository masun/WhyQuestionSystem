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

class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[ [random()*255 for i in range(FV_size)] for x in range(width)] for y in range(height)])

    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, iterations=1000, train_vector=[[]]):
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        
        for i in range(1, iterations+1):

            '''if i % 10 == 0:
                                                    try:
                                                        from PIL import Image
                                                        print "\nSaving Image: sompy_test_colors.png..."
                                                        img = Image.new("RGB", (width, height))
                                                        for r in range(height):
                                                            for c in range(width):
                                                                img.putpixel((c,r), (int(self.nodes[r,c,0]), int(self.nodes[r,c,1]), int(self.nodes[r,c,2])))
                                                        img = img.resize((width*10, height*10),Image.NEAREST)
                                                        img.save("2_sompy_test_colors"+str(i)+".png")
                                                    except:
                                                        print "Error saving the image, do you have PIL (Python Imaging Library) installed?"
                                    
                                                '''
            delta_nodes.fill(0)
            radius_decaying=self.radius*exp(-1.0*i/time_constant)

            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying=self.learning_rate*exp(-1.0*i/time_constant)

            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations))
            
            for j in range(len(train_vector)):
                best = self.best_match(train_vector[j])
                for loc in self.find_neighborhood(best, radius_decaying):

                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    #sys.stdout.write("Influence: " + "/" + str(influence) + "\n")
                    inf_lrd = influence*learning_rate_decaying
                    
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
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
        #print self.nodes
        #print target_FV
        #exit(-1)
        loc = scipy.argmin((((self.nodes - target_FV)**2).sum(axis=2))**0.5)

        r = 0
        while loc > self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5


def random_matrix(nc,nf):
    return [[round(random()*100) for x in range(nc)] for y in range(nf)]

if __name__ == "__main__":
    print "Initialization..."
    colors = [ [0, 0, 0], [100, 100, 100], [100, 0, 0], [255, 100, 50], [10, 20, 100], [40, 255, 10], [150, 30, 90], [7, 1, 200], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
       
    ejemplo = random_matrix(100,100)
    
    
    width = 4
    height = 4
    color_som = SOM(width,height,100,0.05)
    print "Training..."

    for e in ejemplo:
        print e
    color_som.train(1000, ejemplo)
        





            