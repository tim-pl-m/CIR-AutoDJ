#!/usr/bin/python3

import random
from random import randint
from random import uniform

import numpy as np
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
  learning_rate
  discount_factor

  #matrix definitions
  skalierung = 3
  number_of_vertices = genres.length * skalierung

  #create matrix
  matrix = [[0] * number_of_vertices for _ in range(number_of_vertices)]

  def add_edge(self, v1, v2):
      #in first iteation undirected
      # TODO consider directed
            value = 1
            #TODO add q-learning-value
            matrix[v1][v2] = value
            matrix[v2][v1] = value
            #TODO adjust slightly all values for the genre
            #TODO think about this

  def getNextParamters(self):
    # getRandomParamters()

    genre =
    bpm =
    #TODO consider reduction to genre+bpm
    energy = uniform(0, 1)
    vallance = uniform(0, 1)

    print(genres[0][0])
    print(energy)
    print(bpm)
    # TODO fix genre-representation
    return self.genres, energy, vallance, bpm
# Genre(String aus der Liste genres), Energy(0-1), Vallance(0-1), Beats per Minute(60-180)

  # Current percieved mood between 0 and 1 (float)
  def learn(self, mood):
    pass

def getRandomParamters(self):
    random.shuffle(self.genres)
    energy = uniform(0, 1)
    vallance = uniform(0, 1)
    bpm = randint(60, 180)
    return self.genres, energy, vallance, bpm