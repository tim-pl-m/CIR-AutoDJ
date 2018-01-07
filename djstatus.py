from threading import Lock
 
__current_song = None
  
__current_vote = 0
__current_vote_count = 0
  
__current_webcam_mood = 0
  
__lock = Lock()
    
  
def clear_vote():
  global __lock
  global __current_vote
  global __current_vote_count
  
  __lock.acquire()
  __current_vote = 0
  __current_vote_count = 0
  __lock.release()

def vote(increase):
  global __lock
  global __current_vote
  global __current_vote_count
  
  __lock.acquire()
  if __current_vote + increase > 0 :
    __current_vote += increase
  else:
    __current_vote = 0
  __current_vote_count += 1
  __lock.release()

def webcam_mood(mood):
  global __lock
  global __current_webcam_mood
  
  __lock.acquire()
  __current_webcam_mood = mood
  __lock.release()

def get_mood():
  global __current_webcam_mood
  return __current_webcam_mood

def get_vote():
  global __current_vote
  global __current_vote_count
  if __current_vote_count > 0:
    return float(int(float(__current_vote) / __current_vote_count * 100)) / 100
  else:
    return 0

def get_votestats():
  global __current_vote
  global __current_vote_count
  return [__current_vote, __current_vote_count]

def set_song(song):
  global __lock
  global __current_song
  __lock.acquire()
  __current_song = song
  __lock.release()

def get_song():
  global __current_song
  return __current_song
