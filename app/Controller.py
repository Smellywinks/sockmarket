import os
import webapp2
import logging
import calendar
import uuid
import nltk

from google.appengine.ext.webapp import template
from google.appengine.api import users             
from google.appengine.api import mail 
from google.appengine.api import memcache   
from google.appengine.api import search  
from google.appengine.ext import db 
from google.appengine.ext import blobstore   
  
from google.appengine.ext.webapp import blobstore_handlers     

from datetime import date
from datetime import time

# logging setup
# TODO set to INFO in production
logging.getLogger(__name__).setLevel(logging.DEBUG)


# General Utilities
###NONE###

def generateID() :
    return str(uuid.uuid4())
    
def generateEventID() :
    return str(uuid.uuid4())
    
def renderTemplate(response, templatename, templatevalues) :
    basepath = os.path.split(os.path.dirname(__file__)) #extract the base path, since we are in the "app" folder instead of the root folder
    path = os.path.join(basepath[0], 'templates/' + templatename)
    html = template.render(path, templatevalues)
    logging.debug(html)
    response.out.write(html)

def handle404(request, response, exception) :
    """ Custom 404 error page """
    logging.debug('404 Error GET request: ' + str(request))
    logging.exception(exception)
    
    template_values = {
        'page_title' : "Page Not Found",
        'current_year' : date.today().year
    }
        
    renderTemplate(response, '404.html', template_values)

# Handler classes
class AboutHandler(webapp2.RequestHandler) :
    """Request handler for about page"""

    def get(self):
        logging.debug('AboutHandler GET request: ' + str(self.request))
        template_values = {
            'page_title' : "About Sock Market",
            'current_year' : date.today().year,
            'user' : getCurrentUserData()
        }

        renderTemplate(self.response, 'about.html', template_values)

class ErrorHandler(webapp2.RequestHandler):
    """Request handler for error pages"""

    def get(self):
        logging.debug('ErrorHandler GET request: ' + str(self.request))

        template_values = {
            'page_title' : "Oh no...",
            'current_year' : date.today().year
        }
        
        renderTemplate(self.response, 'error.html', template_values)

class IntroHandler(webapp2.RequestHandler):
    """RequestHandler for initial intro page"""

    def get(self):
        """Intro page GET request handler"""
        logging.debug('IntroHandler GET request: ' + str(self.request))

        template_values = {
            'page_title' : "Sock Market",
            'current_year' : date.today().year
        }
            
        renderTemplate(self.response, 'index.html', template_values)
        
    def handle_exception(self, exception, debug):
        # overrides the built-in master exception handler
        logging.error('Template mapping exception, unmapped tag: ' + str(exception))
        
        return self.redirect(uri='/error', code=307)
        
        
# list of URI/Handler routing tuples
# the URI is a regular expression beginning with root '/' char
routeHandlers = [
    (r'/about', AboutHandler),
    (r'/error', ErrorHandler),
    (r'/', IntroHandler),
    (r'/search', SearchHandler),
    (r'/.*', ErrorHandler)
]

# application object
application = webapp2.WSGIApplication(routeHandlers, debug=True)

application.error_handlers[404] = handle404
