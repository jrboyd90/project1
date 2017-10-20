import tornado.log
import tornado.ioloop
import tornado.web
import requests

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

        first_name = self.get_body_argument('first_name')
        last_name = self.get_body_argument('last_name')
        address = self.get_body_argument('address1')
        postalcode = self.get_body_argument('postalcode')
        phone = self.get_body_argument('phone')
        email = self.get_body_argument('email')
        description = self.get_body_argument('description')
        people = self.get_body_argument('people_needed')
        truck = self.get_body_argument('truck_needed')





        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

        params = {
            'address': address,
            'key': 'AIzaSyDICJB-ecPiyM2GtrlleYblXt318jz71So'

        }

        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        result = res['results'][0]

        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']

        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

        row = Request.create(
            first_name = first_name,
            last_name = last_name,
            address1 = address,
            city = 'houston',
            state = 'Texas',
            postalcode = postalcode,
            latitude = lat,
            longitude = lng,
            phone = phone,
            email = email,
            description = description,
            people_needed = people,
            truck_needed = truck

        )
        row.save()

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
