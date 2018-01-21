#!/usr/bin/python3

import random
import operator
from random import randint
from random import uniform

# import numpy as np
from collections import defaultdict


class learning(object):

  matrix = None
  learning_rate = None
  discount_factor = None
  numberOfVertices = None
  genres = []
  bpm = [80, 120, 160]
  actual_state_x = 0
  actual_state_y = 0

  def __init__(self):
    global matrix
    global learning_rate
    global discount_factor
    global numberOfVertices
    global genres
    global bpm
    
    f = open('genres', 'r')
    genres = f.readlines()
    for i in range(len(genres)):
      genres[i] = genres[i].strip()
    f.close()  

    # q-learning parameter
    learning_rate = 0.01
    discount_factor = 0

    #matrix definitions
    numberOfVertices = len(genres) * len(bpm)

    #create matrix
    matrix = [[0] * numberOfVertices for _ in range(numberOfVertices)]

  
  def maxQ(self, x, y):
    # TODO adjust if discount_factor implemented
    return 0
        
  def adjustEdgeAndMatrix(self, x, y, reward):
    global matrix
    
    #in first iteation undirected
    old_value = matrix[x][y]
    # plain q-learning forumla here
    new_value = (1-learning_rate)*old_value + learning_rate*(reward + discount_factor*maxQ(x,y))

    matrix[x][y] = new_value
    matrix[y][x] = new_value
  
  def getNextParamters(self):
    global actual_state_x
    global actual_state_y
    global bpm
    global genres
    
    # pick next vertice
    # if matrix[actual_state_x][actual_state_y + 1]
    listOfSurroundingValues =  {'up':matrix[actual_state_x][actual_state_y - 1], 'down':matrix[actual_state_x][actual_state_y + 1], 'right': matrix[actual_state_x + 1][actual_state_y],'left': matrix[actual_state_x - 1 + 1][actual_state_y]}
    newVertice = max(listOfSurroundingValues.iteritems(), key=operator.itemgetter(1))[0]
    # example:
    # stats = {'a':1000, 'b':3000, 'c': 100}
    # max(stats.iteritems(), key=operator.itemgetter(1))[0]
    if newVertice == 'up':
      # actual_state_x = actual_state_x
      actual_state_y = actual_state_y - 1
    if newVertice == 'down':
      # actual_state_x = actual_state_x
      actual_state_y = actual_state_y + 1
    if newVertice == 'right':
      actual_state_x = actual_state_x + 1

    if newVertice == 'left':
      actual_state_x = actual_state_x  -1


    genre_index = int(actual_state / 3)
    bpm_index = actual_state % 3

    return genre[genre_index], bpm[bpm_index]
# Genre(String aus der Liste genres), Energy(0-1), Vallance(0-1), Beats per Minute(60-180)
  
    # Current percieved mood between 0 and 1 (float)
  def learn(self, mood):
    # calculate reward
    adjustEdgeAndMatrix(actual_state_x,actual_state_y, reward)
    pass
  
#  def getRandomParamters(self):
#    random.shuffle(self.genres)
#    energy = uniform(0, 1)
#    vallance = uniform(0, 1)
#    bpm = randint(60, 180)
#    return self.genres[0], energy, vallance, bpm
