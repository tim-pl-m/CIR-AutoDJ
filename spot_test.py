#!/usr/bin/python3

import spot_control

'''
  empty:  bool (if the AutoDJ Playlist should be emptied on start)
  
  Spotify benötigt authorisierung für Apps - beim ersten Start wird daher der Browser geöffnet - man muss sich einloggen und bestätigen dass
  die App Zugriff erhält - danach wird man weitergeleitet auf eine Url (die nicht erreichbar ist). Auf jeden Fall Url in die Shell kopieren.
  Bei den darauf folgenden Ausführungen nicht mehr nötig weil das Cookie gespeichert wird.
'''

sc = spot_control.spot_control(False)

genre = "rock"
energy = 0.5
temp = 120
valence = 1

while True:
  
  '''
    genre: string
    energy: float: 0 - 1
    temp: int 1 - (bpm)
    valence: float 0 - 1
    wait: bool (if the current song should be skipped or waited until it finished)
  '''
  sc.play(genre, energy, temp, valence, False)
  
  new_genre = input("Next Genre: ")
  if new_genre != "":
    genre = new_genre
