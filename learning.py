#!/usr/bin/python3

import random
from random import randint
from random import uniform

import numpy as np
from collections import defaultdict


class learning():

  genres = ["drum-and-bass",
  "edm",
  "electro",
  "electronic",
  "funk",
  "groove"]
  # TODO fill in missing genres from file "genres"

  def getNextParamters(self):
    random.shuffle(self.genres)

    energy = uniform(0, 1)

    vallance = uniform(0, 1)

    bpm = randint(60, 180)

    # print(genres[1])
    # print(energy)
    # print(bpm)
    return self.genres, energy, vallance, bpm
# Genre(String aus der Liste genres), Energy(0-1), Vallance(0-1), Beats per Minute(60-180)

  # Current percieved mood between 0 and 1 (float)
  def learn(self, mood):
    pass

