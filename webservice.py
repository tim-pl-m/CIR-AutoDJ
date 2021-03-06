from http.server import BaseHTTPRequestHandler, HTTPServer
#from _thread import start_new_thread



#from SocketServer import ThreadingMixIn
#from http.server import ThreadingMixIn
#from socketserver import ThreadingMixIn

import djstatus

#class ThreadingServer(ThreadingMixIn, HTTPServer):
#  pass

class S(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    vote = 0
    request = ''
    if self.path.find("?") > -1:
      request = self.path[self.path.find("?") + 1:]
    request = request.split("&")
    for r in request:
      d = r.split("=")
      if len(d) > 1:
        if d[0] == "vote":
          vote = int(d[1])
          djstatus.vote(vote)
    
    current_song = str(djstatus.get_song())
    display_vote = djstatus.get_vote()
    
    if vote == 1:
      vote = "UP"
    elif vote == -1:
      vote = "DOWN"
    else:
      vote = "N/A"
    
    content = "Current Song:<b>" + current_song + "</b><hr><a href='?vote=1'>UPVOTE</a><br>OverallVote: <b>" + str(display_vote) + "</b><br>Your last vote:" + str(vote) + "<br><a href='?vote=-1'>DOWNVOTE</a>"
    
    self._set_headers()
    self.wfile.write(str.encode("<html><body>" + content + "</body></html>"))

  def do_HEAD(self):
    self._set_headers()
      
  def do_POST(self):
    # Doesn't do anything with posted data
    self._set_headers()
    self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=8080):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('  -W Starting httpd...')
  
  #threading.Thread(target=httpd.serve_forever).start()
  httpd.serve_forever() 
  #ThreadingServer(('', 8080), handler_class).serve_forever()
  
  #start_new_thread(httpd.serve_forever())
  print('  -W End')
  

#if __name__ == "__main__":
#  from sys import argv
#
#  if len(argv) == 2:
#    run(port=int(argv[1]))
#  else:
#    run()
