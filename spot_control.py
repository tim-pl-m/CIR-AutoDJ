#!/usr/bin/python3


import spotipy
import spotipy.util as util
import csv

import random

import time
import pprint

# Workarround
import os
from json.decoder import JSONDecodeError

class spot_control():
  
  __spotify = None
  
  def __init__(self):
    f = open("spotify_credentials", "r")
    c = csv.reader(f)
    for line in c:
      print(line)
      sci = line[0]
      scs = line[1]
      scr = line[2]
      scu = line[3]
      break
    f.close()
    
    try:
      token = util.prompt_for_user_token(username=scu, client_id = sci, client_secret=scs, redirect_uri=scr, scope='user-modify-playback-state')
    except (AttributeError, JSONDecodeError):
      os.remove(f".cache-{scu}")
      token = util.prompt_for_user_token(username=scu, client_id = sci, client_secret=scs, redirect_uri=scr, scope='user-modify-playback-state')
      
    self.__spotify = spotipy.Spotify(auth=token)

  def test(self):
    print('SEEDS ----------')
    genre_seeds = self.__spotify.recommendation_genre_seeds()["genres"]
    print(genre_seeds)

    pp = pprint.PrettyPrinter()

    while True:

      genre = genre_seeds[random.randint(0, len(genre_seeds) - 1)]

      # acousticness
      # danceability = 1
      # duration_ms
      # * energy
      # instrumentalness
      # # key
      # liveness = 0
      # * loudness
      # # mode
      # popularity
      # * speechiness
      # * tempo
      # # time_signature
      # * valence


      # Variabel:
      tempo = 120
      danceability = 1
      
      # Fixed:
      valence = 1
      liveness = 0
      
      recommendations = self.__spotify.recommendations(seed_genres=[genre], limit=1, target_danceability=danceability, target_liveness=liveness, target_valence=valence, target_tempo=tempo) # , target_tempo=tempo, target_danceability=danceability, target_liveness=liveness, target_valence=valence
      print('RECOMMENDATIONS ----------' + genre)
      #pp.pprint(recommendations)
      
      print(recommendations['tracks'][0]["artists"][0]["name"])
      print(recommendations['tracks'][0]["album"]["name"])
      print(recommendations['tracks'][0]["name"])
    
      time.sleep(1)
    
    #search = self.__spotify.search("artist:muse", type="artist")
    
    #print('SEARCH ----------')
    #print(search)
    
    print("End")
    
    
