#!/usr/bin/env python

#  Routes
#  /
#  /board/new
#  /update


#  Decorators
#  @login_required

import os

# They are changing Django version, need to include this
# http://code.google.com/appengine/docs/python/tools/libraries.html#Django
#from google.appengine.dist import use_library
#use_library('django', '1.2')
from google.appengine.ext.webapp import template

import wsgiref.handlers, logging
import cgi, time, datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from usermodels import *  #I'm storing my models in usermodels.py


class MainHandler(webapp.RequestHandler):
  def get(self):
    leaders = LeaderBoard.gql('where game_id=101 order by score limit 5') 
    
    template_values = {
      'leaders': leaders,
      'game_id': '101'
    }

    render_template(self, 'templates/index.html', template_values)

class UpdateHandler(webapp.RequestHandler):
  def post(self):
    l = LeaderBoard()
    l.username = self.request.get('username') 
    l.score = int(self.request.get('score'))
    l.game_id = int(self.request.get('game_id')) 
    l.put()

class BoardHandler(webapp.RequestHandler):
  def get(self):
    b = Board()
    b.id = 101
    b.positions = 'td_3 td_2 td_1 td_6 td_5 td_4 td_8 td_7'
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
                                        ('/board/new', BoardHandler)],
                                         debug = is_local())
                                         
  
  from gae_mini_profiler import profiler
  application = profiler.ProfilerWSGIMiddleware(application)

  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
