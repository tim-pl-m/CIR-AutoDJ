#!/usr/bin/python3

import random
import operator
from random import randint
from random import uniform

# import numpy as np
from collections import defaultdict


class learning():

  genres = [
  # "drum-and-bass",
  # "edm",
  "indie",
  # "punk",
  "reggaeton",
  # "electronic",
  # "funk",
  # "groove",
  "electro"
  ]
  # TODO consider fill in missing genres from file "genres"

  # q-learning parameter
  learning_rate = 0.01
  #TODO consider not myoptic(so make it longer sighted)
  discount_factor = 0

  #matrix definitions
  #subdivide genres
  scaling = 3
  number_of_vertices = genres.length * scaling

  #create matrix
  matrix = [[0] * number_of_vertices for _ in range(number_of_vertices)]

  #save actual vertice
  # TODO consider starting from a random state
  actual_state_x = 0
  actual_state_y = 0

  def maxQ(self, x, y):
      # TODO adjust if discount_factor implemented
    return 0
  def adjustEdgeAndMatrix(self, x, y, reward):
      #in first iteation undirected
      # TODO consider directed
            old_value = matrix[x][y]
            # plain q-learning forumla here
            new_value = (1-learning_rate)*old_value + learning_rate*(reward + discount_factor*maxQ(x,y))

            matrix[x][y] = new_value
            matrix[y][x] = new_value
            #TODO consider to adjust slightly all values for this genre
            #TODO test this first!
            # if new_value > 0:
            #     for x in range(0, 3):
            #         for y in range(0, 3):
            # if new_value < 0:
            #TODO think about this

  def getNextParamters(self):
    # pick next vertice
    # TODO maybe catching errors is needed here
    # TODO consider improvement
    # TODO consider 8 values instead of 4 to speed up decision
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


    #interpret matrix
    # TODO make dynamic
    # genre:
    # TODO check if genres[0]
    if actual_state_x < 3:
        genre = genres[0][0]
    # bpm:
    bpm =
    #TODO consider reduction to genre+bpm
    #pick unlearned values randomly
    energy = uniform(0, 1)
    vallance = uniform(0, 1)

    # getRandomParamters()
    print(genres[0][0])
    print(energy)
    print(bpm)
    # TODO fix genre-representation
    return self.genres, energy, vallance, bpm
# Genre(String aus der Liste genres), Energy(0-1), Vallance(0-1), Beats per Minute(60-180)

  # Current percieved mood between 0 and 1 (float)
  def learn(self, mood):
    # calculate reward
    # TODO
    # adjust old value with reward
    adjustEdgeAndMatrix(actual_state_x,actual_state_y, reward)
    pass

def getRandomParamters(self):
    random.shuffle(self.genres)
    energy = uniform(0, 1)
    vallance = uniform(0, 1)
    bpm = randint(60, 180)
    return self.genres, energy, vallance, bpm