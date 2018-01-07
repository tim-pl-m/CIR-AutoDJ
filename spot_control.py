#!/usr/bin/python3


import spotipy
import spotipy.util as util
import csv

import random

import time
import pprint

import djstatus

# Workarround
import os
from json.decoder import JSONDecodeError

class spot_control():
  pp = pprint.PrettyPrinter()
  
  __spotify = None
  __playlist_id = None
  __user_id = None
  __played_song_ids = []
  
  __rec_limit = 1
  __rec_last_genre = None
  
  __possible_grenres = []
  
#  __djstatus = None
  
  def __init__(self, empty = True):
    
    #self.__djstatus = djstatus
    
    #print(os.path.dirname(spotipy.__file__))
    
    f = open("spotify_credentials", "r")
    c = csv.reader(f)
    for line in c:
      if len(line) >= 3:
        sci = line[0]
        scs = line[1]
        scr = line[2]
      if len(line) == 4:
        scu = line[3]
      else:
        scu = input("Please provide spotify username: ")
      break
    f.close()
    
    f = open('genres', 'r')
    genres = f.readlines()
    for i in range(len(genres)):
      genres[i] = genres[i].strip()
    f.close()  
    
    scope = ['user-modify-playback-state', 'playlist-read-private', 'playlist-modify-private', 'user-read-currently-playing', 'user-read-playback-state', 'playlist-modify-private']
    scope = " ".join(scope)
    
    #try:
    token = util.prompt_for_user_token(username=scu, client_id = sci, client_secret=scs, redirect_uri=scr, scope=scope)
    #except (AttributeError, JSONDecodeError):
    #  os.remove(f".cache-{scu}")
    #  token = util.prompt_for_user_token(username=scu, client_id = sci, client_secret=scs, redirect_uri=scr, scope=scope)
    
    self.__user_id = scu
    
    self.__spotify = spotipy.Spotify(auth=token)
    
    # Search for autodj playlist
    
    tracks = None
    playlists = self.__spotify.current_user_playlists()
    for l in playlists['items']:
      if l['name'] == "AutoDJ":
        print("  -S Found Playlist: " + l['id'])
        # self.pp.pprint(l)
        
        self.__playlist_id = l['id']
        # Get Tracks
        tracks = self.__spotify.user_playlist_tracks(self.__user_id, self.__playlist_id) #l['tracks']['href']
        
        # self.pp.pprint(tracks)
        break
    
    if self.__playlist_id == None:
      print("  -S Creating Playlist ...")
      playlist = self.__spotify.user_playlist_create(user=self.__user_id, name="AutoDJ", public=False)
      
      # self.pp.pprint(playlist)
      
      if 'id' in playlist:
        self.__playlist_id = playlist['id']
      else:
        print("  @S Could not create playlist")
        exit(1)
    
    # Empty playlist
    if empty and tracks != None:
      print("  -S Deleting all tracks from playlist")
      track_uris = []
      #self.pp.pprint(tracks)
      for t in tracks['items']:
        track_uris.append(t['track']['uri'])
      
      self.__spotify.user_playlist_remove_all_occurrences_of_tracks(self.__user_id, self.__playlist_id, track_uris)
      tracks = None
    
    # Taking tracks into already played ...
    if tracks != None:
      for t in tracks['items']:
        #self.pp.pprint(t)
        
        self.__played_song_ids.append(t['track']['id'])
    
    
    self.__possible_grenres = self.__spotify.recommendation_genre_seeds()["genres"]
    
    for i in range(len(genres) - 1, -1, -1):
      if genres[i] not in self.__possible_grenres:
        del genres[i]
    
    self.__possible_grenres = genres
    
    #print("Possible Genres:")
    #print(self.__possible_grenres)
    #methodList = [method for method in dir(self.__spotify) if callable(getattr(self.__spotify, method))]
    #print(methodList)
    #input()
    

  def play(self, genre, energy, tempo, valence, wait = True):
    
    if genre not in self.__possible_grenres:
      print("  @S " + str(genre) + " not available: ")
      print(self.__possible_grenres)
      return
    
    
    if self.__rec_last_genre != genre:
      self.__rec_last_genre = genre
      self.__rec_limit = 1
    
    next_track = None
    print("  -S Get recommendations")
    while next_track == None:
      #print("* Get recommendations (" + str(self.__rec_limit) + ")")
      seed_tracks = None
      
      if self.__rec_limit > 1 and len(self.__played_song_ids) > 0:
        recommendations = self.__spotify.recommendations(seed_tracks=self.__played_song_ids[-5:], limit=self.__rec_limit, target_energy=energy, target_tempo=tempo, target_valence=valence)
      else:
        recommendations = self.__spotify.recommendations(seed_genres=[genre], limit=self.__rec_limit, target_energy=energy, target_tempo=tempo, target_valence=valence)
      
      if len(recommendations['tracks']) == 0:
        print("  @S Did not get any recommendations")
      
      for r in recommendations['tracks']:
        if r['id'] not in self.__played_song_ids:
          #print("* Found " + str(r["id"]))
          next_track = r
          break
        else:
          pass
          #print("* Played already: " + str(r["id"]))
      
      if next_track == None:
        self.__rec_limit = self.__rec_limit * 2
        #print("* Setting Limit to: " + str(self.__rec_limit))
      
      
    #print('* Recommendation ----------')
    #print(next_track['id'])
    #print(next_track["artists"][0]["name"])
    #print(next_track["album"]["name"])
    #print(next_track["name"])
    #print('                 ----------')
    print('  -S Append to Playlist ' + str(next_track['name']))
    self.__spotify.user_playlist_add_tracks(self.__user_id, self.__playlist_id, [next_track['id']])
    self.__played_song_ids.append(next_track['id'])
    
    if wait:
      #current_track = self.__spotify.current_user_playing_track()
      current_track = self.__spotify.current_playback()
      #self.pp.pprint(current_track)
      if not current_track == None and current_track['is_playing']:
        progress = current_track['progress_ms']
        length = current_track['item']['duration_ms']
        wait = length - progress
        print("  -S Sleeping for " + str(wait) + " ms")
        time.sleep(wait / 1000)
    
    print("  -S Start playback")
    try:
      self.__spotify.start_playback(uris = [next_track['uri']])
    except spotipy.client.SpotifyException:
      print("  @S Could not start Playback - you need to start Playlist yourself!")

    #self.__djstatus.set_song(next_track['id'] + ":" + next_track['name'])
    #djstatus.set_song(next_track['id'] + ":" + next_track['name'])
    djstatus.set_song(next_track['name'])

    duration=1000
    current_track = self.__spotify.current_playback()
    if current_track != None:
      progress = current_track['progress_ms']
      length = current_track['item']['duration_ms']
      duration = length - progress
    return duration


  def test(self):
    print('SEEDS ----------')
    genre_seeds = self.__spotify.recommendation_genre_seeds()["genres"]
    # print(genre_seeds)

    genre = genre_seeds[random.randint(0, len(genre_seeds) - 1)]

    while True:

      # Variabel:
      tempo = 120
      danceability = 1
      
      # Fixed:
      valence = 1
      liveness = 0
      
      if self.__rec_limit > 1:
        
        seed_tracks = self.__played_song_ids[-5:]
        print("===== Searching with", end=' ')
        print(seed_tracks)
        recommendations = self.__spotify.recommendations(seed_tracks=seed_tracks, limit=self.__rec_limit, target_danceability=danceability, target_liveness=liveness, target_valence=valence, target_tempo=tempo)
      else:
        print("===== Searching for " + genre)
        recommendations = self.__spotify.recommendations(seed_genres=[genre], limit=self.__rec_limit, target_danceability=danceability, target_liveness=liveness, target_valence=valence, target_tempo=tempo) # , target_tempo=tempo, target_danceability=danceability, target_liveness=liveness, target_valence=valence
      
      next_track = None
      for r in recommendations['tracks']:
        if r['id'] not in self.__played_song_ids:
          next_track = r
          break
      
      if next_track == None:
        self.__rec_limit = self.__rec_limit * 2
        print("* Setting Limit to: " + str(self.__rec_limit))
      else:
        self.__rec_limit = 1
        print('RECOMMENDATION ----------' + genre)
        print(next_track['id'])
        print(next_track["artists"][0]["name"])
        print(next_track["album"]["name"])
        print(next_track["name"])
        self.__played_song_ids.append(next_track['id'])
    
      time.sleep(1)
    
    print("End")
