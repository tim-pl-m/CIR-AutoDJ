#!/usr/bin/python3

import random
import operator
from random import randint
from random import uniform

# import numpy as np
from collections import defaultdict


class learning():

  matrix = None
  learning_rate = None
  discount_factor = None
  numberOfVertices = None
  genres = []
  bpm = [80, 120, 160]
  actual_state_x = 0
  actual_state_y = 0

  def __init__(self):
    
    f = open('genres', 'r')
    self.genres = f.readlines()
    for i in range(len(self.genres)):
      self.genres[i] = self.genres[i].strip()
    f.close()  

    # q-learning parameter
    self.learning_rate = 0.01
    self.discount_factor = 0

    #matrix definitions
    self.numberOfVertices = len(self.genres) * len(self.bpm)

    #create matrix
    self.matrix = [[0] * self.numberOfVertices for _ in range(self.numberOfVertices)]

  
  def maxQ(self, x, y):
    # TODO adjust if discount_factor implemented
    return 0
        
  def adjustEdgeAndMatrix(self, x, y, reward):
    
    #in first iteation undirected
    old_value = self.matrix[x][y]
    # plain q-learning forumla here
    new_value = (1-self.learning_rate)*old_value + self.learning_rate*(reward + self.discount_factor*self.maxQ(x,y))

    self.matrix[x][y] = new_value
    self.matrix[y][x] = new_value
  
  def getNextParamters(self):
    
    # pick next vertice
    # if matrix[actual_state_x][actual_state_y + 1]
    listOfSurroundingValues =  {'up':self.matrix[self.actual_state_x][self.actual_state_y - 1], 'down':self.matrix[self.actual_state_x][self.actual_state_y + 1], 'right': self.matrix[self.actual_state_x + 1][self.actual_state_y],'left': self.matrix[self.actual_state_x - 1 + 1][self.actual_state_y]}
    # newVertice = max(listOfSurroundingValues.iteritems(), key=operator.itemgetter(1))[0]
    
    newVertice = None
    newValue = None
    for key in listOfSurroundingValues:
      if newValue == None or listOfSurroundingValues[key] > newValue:
        newVertice = key
        newValue = listOfSurroundingValues[key]
    
    # example:
    # stats = {'a':1000, 'b':3000, 'c': 100}
    # max(stats.iteritems(), key=operator.itemgetter(1))[0]
    if newVertice == 'up':
      # actual_state_x = actual_state_x
      self.actual_state_y = self.actual_state_y - 1
    if newVertice == 'down':
      # actual_state_x = actual_state_x
      self.actual_state_y = self.actual_state_y + 1
    if newVertice == 'right':
      self.actual_state_x = self.actual_state_x + 1

    if newVertice == 'left':
      self.actual_state_x = self.actual_state_x  -1


    genre_index = int(self.actual_state_x / 3)
    bpm_index = self.actual_state_x % 3

    return self.genres[genre_index], self.bpm[bpm_index]
# Genre(String aus der Liste genres), Energy(0-1), Vallance(0-1), Beats per Minute(60-180)
  
    # Current percieved mood between 0 and 1 (float)
  def learn(self, reward):
    # calculate reward
    self.adjustEdgeAndMatrix(self.actual_state_x,self.actual_state_y, reward)
  
#  def getRandomParamters(self):
#    random.shuffle(self.genres)
#    energy = uniform(0, 1)
#    vallance = uniform(0, 1)
#    bpm = randint(60, 180)
#    return self.genres[0], energy, vallance, bpm
