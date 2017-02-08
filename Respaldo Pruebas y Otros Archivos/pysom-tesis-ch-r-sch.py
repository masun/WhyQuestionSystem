"""
======================================================================
Python Self-Organizing Maps 
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
----------------------------------------------------------------------
* Copyright (c) 2006-2008, Charles R. Schmidt
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above
*       copyright notice, this list of conditions and the following
*       disclaimer in the documentation and/or other materials
*       provided with the distribution.
*     * Neither the name of the San Diego State University nor the
*       names of its contributors may be used to endorse or promote
*       products derived from this software without specific prior
*       written permission.
*
* THIS SOFTWARE IS PROVIDED BY Charles R. Schmidt ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
* PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Charles R. Schmidt BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
* BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
* LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
* NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
======================================================================
"""
# Standard Libraries
import random,math,time,sys,os
from math import acos,sqrt,pi,degrees,sin,cos,asin
import pickle #provides object serialization

# External Libraries
# http://numpy.scipy.org/
from numpy import array,empty,take,put,zeros
import numpy as N
# https://networkx.lanl.gov/
import networkx as NX

# Local Libraries (part of pySom)
import networkFunctions as nf
from data import ObsFile

class som:
    ''' Base class for the Self-Organizing Map,
        Each topology will inherit from this class.
        A template is provided in 'Topology'
    '''
    def __init__(self):
        '''
        These initial training parameters should be
        set before training.
        '''
        # int, the number of dimension in the input-space
        self.Dims = 0
        # int, optionally the number neurons in the X dimension
        self.X = 0
        # int, optionally the number neurons in the Y dimension
        self.Y = 0
        # int, total number of neurons
        self.Size = 0
        # str, name of topology type
        self.Type = 'none'
        # int, total number of training steps.
        self.tSteps = 0
        # float, initial neighborhood radius, expressed as percentage.
        self.maxN = 0.0
        # float, initial learning rate
        self.alpha0 = 0.0

        # reference vectors are stored here.
        self.nodes = []
        # mapping of observations to neurons is stored here.
        self.daMap = {}

    def load(self,path='',name=None):
        ''' This function loads a saved SOM from disk into memory.
            pySom uses several files to represent the SOM,
            .cod is the Codebook file which represents the
                reference vectors
            .map represents the mapping of the observations
                onto the trained SOM
            
            If the path and name are omitted they will be guessed 
            based on the SOM's parameters
        '''
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.cod'
        mapname = path+name+'.map'
        if os.path.exists(mapname):
            try:
                f = open(mapname,'r')
                self.daMap = pickle.load(f)
                f.close()
            except:
                self.daMap = {}
        dataf = open(codname,'r')
        header = dataf.next()
        Dims,Type,x,y,nType= header.split()
        self.Dims = int(Dims)
        self.Type = Type
        self.X, self.Y = int(x),int(y)
        self.Size = self.X*self.Y
        self.nodes = array([[0.0 for i in xrange(self.Dims)] for j in xrange(self.Size)])
        for i in xrange(self.Size):
            data = dataf.next()
            data = data.split()
            data = map(float,data)
            self.nodes[i] = data

    def save(self,path='',name=None):
        ''' This function saves a SOM to disk.
            pySom uses several files to represent the SOM,
            .cod is the Codebook file which represents the
                reference vectors
            .map represents the mapping of the observations
                onto the trained SOM
            
            If the path and name are omitted they will be guessed 
            based on the SOM's parameters
        '''
        if self.X == 0 or self.Y == 0:
            self.X = self.Size
            self.Y = 1
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.cod'
        mapname = path+name+'.map'
        if self.daMap:
            mapfile = open(mapname,'w')
            pickle.dump(self.daMap,mapfile)
            mapfile.close()
        outf = open(codname,'w')
        outf.write("%d %s %d %d gaussian\n"%(self.Dims,self.Type,self.X,self.Y))
        for i in xrange(self.Size):
            outf.write(' '.join(str(self.nodes[i].tolist())[1:-1].split(', '))+'\n')
        outf.close()

    def randInit(self):
        ''' This function initializes the reference vectors with
            random values in the range of 0 to 1.  If your data has
            not standardized within this range, this function should
            be overwritten.
    
            * Ideally this function would analyze the input data and
              scale the randomization accordingly.  SOM_PAK does 
              something along these lines, their code might help find
              a good solution for this.
        '''
        self.nodes = array([[random.random() for j in xrange(self.Dims)] for i in xrange(self.Size)])

    def findBMU(self,ind,v,ReturnDist = False):
        ''' This function returns the ID of the reference vector that
            is the closest (in Euclidean distance) to input vector v.
            Optionally this function will also return that distance
            between the two.  Overwrite this function if you need
            something other than Euclidean dist.

            the 'ind' parameter is unused and should be set to None.

            * As written this function does not handle missing values,
              a previous version did, but it was painfully slow. One
              option would be to remove the distance function and pick
              the appropriate dist function depending on the values
              present.
            * An external distance function could also be used here,
              however the extra function call will effect
              performance.
        '''
        d = ((self.nodes-v)**2).sum(1)
        minI = d.argmin()
        if ReturnDist:
            minD = d[minI]
            return minI,minD
        else:
            return minI

    def alpha(self,t):
        ''' Returns the learning rate (alpha) as a function of time t.
        '''
        r = self.alpha0 * (1 - (t/float(self.tSteps)))
        if r < 0: r = 0
        return r
    def hci(self, t, dist):
        ''' This kernel function adjust the magnitude with which the
            observation affects the reference vectors.
        '''
        sigma = self.kernelWidth(t)
        a = self.alpha(t)
        top = dist**2
        bottom = (2*(float(sigma)**2))
        return a * math.exp(-top/bottom)

    def merge(self,t,ind,v):
        ''' This function adjusts the actual reference vectors at time
            't' based on observation vector 'v'.
        '''
        bmu = self.findBMU(None,v)
        sigma = self.kernelWidth(t)
        results = self.neighborhood( bmu , sigma )
        alteredNodes = [(results[i],self.hci(t,self.odist(i))) for i in xrange(len(results))]
        for nodeID,hc in alteredNodes:
            if len(ind) == self.Dims:
                part = self.nodes[nodeID]
                delta = hc*(v-part)
                self.nodes[nodeID] = part+delta
            else:
                part = take(self.nodes[nodeID],ind)
                delta = hc*(v-part)
                put(self.nodes[nodeID],ind,part+delta)

    def run(self,obsf):
        ''' Call this function with your observation file are a
            parameter.

            obsf must be an instance ObsFile as provided by data.py

            All training parameters should be set before calling this
            function.
        '''
        self.neighborhoodCache = {}
        print "####################################"
        print "###        Configuration         ###"
        print "####################################"
        print "  N = %d, maxN = %f"%(self.Size,self.maxN)
        print "  Total runs: %d"%self.tSteps
        print "  initial learning rate = %f"%self.alpha0
        print "  Obs File:%s"%obsf.filename
        print "####################################"
        print "###          End Config          ###"
        print "####################################"
        print ""
        print "Running..."
        t1 = time.time()
        T = self.tSteps
        for t in xrange(self.tSteps):
            id,ind,v = obsf.stream()
            self.merge(t,ind,v)
            sys.stdout.write("\r%.2f%%"%(100*float(t)/T))
            sys.stdout.flush()
        print "\nRun completed in %f seconds"%(time.time()-t1)

    def map(self,obsf):
        ''' This function maps the observation back onto the trained
            SOM.  The QError is returned.
        '''
        qerror = 0
        counter = 0 
        daMap = {} # keys are node ID's, values are lists of observation ID's.
        for id,dimIds,obs in obsf:
            bm,err = self.findBMU(dimIds,obs,ReturnDist=True)
            qerror += err
            if not bm in daMap:
                daMap[bm] = []
            daMap[bm].append(id)
            sys.stdout.write(".%d,%f.\r"%(counter,err))
            sys.stdout.flush()
            counter += 1
        print ""
        qerror = qerror/counter
        self.daMap = daMap
        return qerror
    def umat(self, options = ''):
        """
        Calculate the U-Matrix

        Parameters:
        options -- str -- ['', 'average', 'median']
            If provided the average or median distances will be computed, otherwise the sum of distances is returned.
        """
        u = [0.0 for nid in xrange(self.Size)]
        for nid in xrange(self.Size):
            vec = self.nodes[nid]
            neighbors = self.neighborhood(nid,1)
            neighbors = [xid for xid in neighbors.keys() if xid!=nid]
            if options == 'median':
                d = N.median( (((self.nodes[neighbors]-vec)**2).sum(1)) ** (0.5) )
            elif options == 'average':
                d = N.mean( ((((self.nodes[neighbors]-vec)**2).sum(1)) ** (0.5)) )
            else:
                d = ((((self.nodes[neighbors]-vec)**2).sum(1)) ** (0.5)).sum()
            #print nid,d
            u[nid] = d
        return u
        
    
class GraphTopology(som):
    ''' GraphTopology extends "som" and provides a functioning
        implementation of the Self-Organizing Map training algorithm.
        The topology is based on a graph structure with is provided
        using the NetworkX graph library.
    '''
    def __init__(self,G=None,Type='Graph'):
        ''' Special initialization for this topology,
            also calls som.__init__
        '''
        som.__init__(self)
        self.Type = Type
        if G:
            self.G = G

            # Number of nodes (neurons) in the network.
            self.Size = G.order()
            # if findWidth is not given a seed it will brute force the
            # total network width, this could take a long time. For
            # the spherical network, one of the polls should yield the
            # correct width. Or possibly the node with lowest degree.
            # The Width messures the largest distance between any two
            # nodes in the network.

            self.Width = nf.findWidth(G,G.nodes()[-1]) 

    def save(self,path,name):
        ''' in addition to saving this codebook, we also need to save
            the graph
        '''
        som.save(self,path,name)
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        graphFile = path+name+'.graph'
        f = open(graphFile,'wb')
        pickle.dump(self.G,f) #serialize the graph to a textfile.
        f.close()
    def load(self,path,name):
        ''' loads the graph and other information from disk '''
        som.load(self,path,name)
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        graphFile = path+name+'.graph'
        if os.path.exists(graphFile):
            f = open(graphFile,'rb')
            self.G = G = pickle.load(f)
            self.Size = G.order()
            self.Width = nf.findWidth(G,G.nodes()[-1]) 
            f.close()
    def kernelWidth(self,t):
        ''' kernelWidth returns the width of the neighborhood in terms
            of order.
        '''
        r = round((self.Width*self.maxN) * (1 - (t/float(self.tSteps))))
        r = int(r)
        if r == 0: r = 1
        return r
    def neighborhood(self,bmu,kernelWidth):
        '''
        This function returns a dictionary containing the neighbors of
        bmu as keys and their dist (as an order) as values.
        '''
        return nf.neighborhood(self.G,bmu,kernelWidth)
    def merge(self,t,ind,v):
        ''' This function adjusts the actual reference vectors at time
            't' based on observation vector 'v'.
        '''
        bmu = self.findBMU(None,v)
        a = self.alpha(t)
        sigma = self.kernelWidth(t)
        results = self.neighborhood( bmu , sigma )
        sigma = float(sigma)

        # hci has been internalized in this next line,
        # to speed up processing
        alteredNodes = [(node,(v-self.nodes[node])*(a*math.exp(-(odist*odist)/(2*sigma*sigma)))) for node,odist in results.iteritems()]
        for nodeID,node in alteredNodes:
            self.nodes[nodeID] += node

#class Topology(som):
#    """ Template class for topology.
#        Copy this class to create a new topology for som.
#    """
#    def __init__(self):
#       som.__init__(self)
#    def save(self,path,name):
#       som.save(self,path,name)
#    def load(self,path,name):
#       som.load(self,path,name)
#    def randInit(self):
#       som.randInit(self)
#    def kernelWidth(self,t):
#       ''' kernelWidth returns the width of the neighborhood in terms
#           of order.
#       '''
#       pass
#    def odist(n):
#       """
#       n is the nth neuron in the in neighborhood, returns order
#       example the 3rd neuron in the set is 1 order from the 0th.
#       """
#       pass
#    def neighborhood(self,bmu,kernelWidth):
#       '''
#       This function returns a dictionary containing the neighbors of
#       bmu as keys and their dist (as an order) as values.
#       '''
#       pass