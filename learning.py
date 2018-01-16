#!/usr/bin/python3

import random
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
  # TODO fill in missing genres from file "genres"

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

  def adjustEdgeAndMatrix(self, x, y, reward):
      #in first iteation undirected
      # TODO consider directed
            old_value = matrix[x][y]
            # plain q-learning forumla here
            new_value = (1-learning_rate)*old_value + learning_rate*(reward+discount_factor*)
            #TODO add q-learning-value
            matrix[x][y] = new_value
            matrix[y][x] = new_value
            #TODO adjust slightly all values for the genre
            #TODO think about this

  def getNextParamters(self):
    # pick next vertice
    # TODO maybe catching errors is needed here
    if matrix[actual_state_x][actual_state_y + 1]

    #interpret matrix
    genre =
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