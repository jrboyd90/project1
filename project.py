import tornado.log
import tornado.ioloop
import tornado.web

from jinja2 import Environment, PackageLoader, select_autoescape
from models import *

# Retrieve path where HTML lives
ENV = Environment(
    loader=PackageLoader('project', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

# Home Page Handler

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

# def retrieve_api_data():






class MainHandler(TemplateHandler):
    def get (self):
      self.set_header('Cache-Control',
       'no-store, no-cache, must-revalidate, max-age=0')
      self.render_template("index.html", {})


class RequestFormHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control',
         'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("request_form.html", {})

    def post(self):
        # Process form data
        self.set_header('Cache-Control',
         'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("request_form.html", {})

class VolunteerFormHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control',
         'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("volunteer_form.html", {})

    def post(self):
        # Process form data
        self.set_header('Cache-Control',
         'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("volunteer_form.html", {})


# Make the Web Applicaton using Tornado
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/request_form", RequestFormHandler),
    (r"/volunteer_form", VolunteerFormHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)

# Main
if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(8888, print('Hosting at 8888'))
    tornado.ioloop.IOLoop.current().start()
