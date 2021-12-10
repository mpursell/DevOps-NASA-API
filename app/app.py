import json
from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

api_key = os.environ.get('API_KEY')

class API_Handler():

    def __init__(self, category: str):
        self._api_key = os.environ.get('API_KEY')
        # category is the category of image - 'apod' or 'Mars' as it stands
        self.category = category
        self.query = {}
        self.camera = 'mast'
    
        
    # choose an endpoint depending on whether "mars" or "apod" is passed in
    # default using a class attribute above to camera=mast
    def get_url(self):

        if self.category == 'apod':
            self.url = 'https://api.nasa.gov/planetary/apod'
            self.query = {'api_key': self._api_key}
            

        elif self.category == 'mars':
            self.url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
            self.query = {'sol':'1000', 'camera': f'{self.camera}', 'api_key':self._api_key}

        return self.url, self.query

    
    def make_request(self) -> json:
        url = self.get_url()
        payload = self.query
        response = requests.get(self.url, params=payload)
        return response

    

class Item:

    def __init__(self):
        self.image_url = ""
        self.image_explanation = ""
        self.image_date = ""
        self.image_title =""
        self.photos = []

    def set_attributes(self, category, response):

        self.response = response

        if category == 'apod':
            self.image_url = self.response['url']
            self.image_title = self.response['title']
            self.image_explanation = self.response['explanation']
            self.image_date = self.response['date']

        elif category == 'mars':
            self.photos = self.response['photos']
            self.image_url = self.photos[0]['img_src']

        

@app.route('/')
def index():

    apiCall = API_Handler('apod')
    response = apiCall.make_request()
    
    response = response.json() 

    # create new Item object 
    item = Item()
    item.set_attributes('apod', response)
    
    # now we've got an object with properties, we can just return that object,
    # rather than a long list of vars.
    return render_template('index.html', item=item)

@app.route('/mars', methods=['GET', 'POST'])
def mars():

    camera = request.form.get('selected')
    
    apiCall = API_Handler('mars')
    apiCall.camera = camera

    response = apiCall.make_request()
    response = response.json()
    
    item = Item()
    item.set_attributes('mars', response)

    # reload after form submission, handle errors if there are no 
    # images returned
    try:
        item.image_url = item.photos[0]['img_src']

    except IndexError:
        # make an API call with the class defaults (camera=mars) if there's nothing in the list of photos

        apiCall = API_Handler('mars')
        response = apiCall.make_request()
        
        response = response.json()
        item = Item()
        item.set_attributes('mars', response)
  

    return render_template('mars.html', item=item)