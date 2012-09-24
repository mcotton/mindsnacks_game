#!/usr/bin/env python

#  Routes
#  /
#  /update
#  /upload


#  Decorators
#  @login_required

import os
import random

from google.appengine.ext.webapp import template

import wsgiref.handlers, logging
import cgi, time, datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from usermodels import *  #I'm storing my models in usermodels.py


class MainHandler(webapp.RequestHandler):
  def get(self):
    lst = []

    b = Board.all()
    for i in b.run():
        lst.append(i.id)

    random.shuffle(lst)

    game_id = lst[0]
    
    leaders = LeaderBoard.gql('where game_id=:1 order by score limit 5', int(game_id)) 

    b = Board.gql('where id=:1', game_id)
    t = b.get()

    template_values = {
      'leaders': leaders,
      'game_id': game_id,
      'table': t.table
    }

    render_template(self, 'templates/index.html', template_values)

class UpdateHandler(webapp.RequestHandler):
  def post(self):
    l = LeaderBoard()
    l.username = self.request.get('username') 
    l.score = int(self.request.get('score'))
    l.game_id = int(self.request.get('game_id')) 
    l.put()

class UploadHandler(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/uploader.html', {})

  def post(self):
    b = Board()
    b.id = self.request.get('id') 
    b.table = self.request.get('table')
    b.put()


def is_local():
  # Turns on debugging error messages if on local env  
  return os.environ["SERVER_NAME"] in ("localhost")  
    
def render_template(call_from, template_name, template_values):
  # Makes rendering templates easier.
  path = os.path.join(os.path.dirname(__file__), template_name)
  call_from.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/update', UpdateHandler),
                                        ('/upload', UploadHandler)],
                                         debug = is_local())
                                         
  
  from gae_mini_profiler import profiler
  application = profiler.ProfilerWSGIMiddleware(application)

  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
