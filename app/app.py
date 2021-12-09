import json
from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

api_key = os.environ.get('API_KEY')

class API_Handler():

    def __init__(self, category: str):
        self._api_key = os.environ.get('API_KEY')
        self.category = category
        self.query = {}
        self.camera = 'mast'
    
        
    # choose an endpoint depending on whether "mars" or "apod" is passed in
    # default to camera=mast
    def get_url(self):
        if self.category == 'apod':
            self.url = 'https://api.nasa.gov/planetary/apod'
            self.query = {'api_key': self._api_key}
            return self.url, self.query
        elif self.category == 'mars':
            self.url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
            self.query = {'sol':'1000', 'camera': f'{self.camera}', 'api_key':self._api_key}

            return self.url, self.query

    def make_request(self) -> json:
        url = self.get_url()
        payload = self.query
        #response = requests.get(f'{url}', params=payload)
        response = requests.get(self.url, params=payload)
        return response

@app.route('/')
def index():

    #response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")

    apiCall = API_Handler('apod')
    response = apiCall.make_request()
    
    response = response.json()
    url = response['url']

    image_title = response['title']
    image_explanation = response['explanation']
    image_date = response['date']

    return render_template('index.html', landing_image=url, image_title=image_title, image_explanation=image_explanation, image_date=image_date)

@app.route('/mars', methods=['GET','POST'])
def mars():

    camera = request.form.get('selected')
    
    apiCall = API_Handler('mars')
    apiCall.camera = camera

    response = apiCall.make_request()
    response = response.json()
    
    photos = response['photos']


    try:
        image_url = photos[0]['img_src']
    except IndexError:
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=mast&api_key={api_key}')

        response = response.json()
        photos = response['photos']
        image_url = photos[0]['img_src']

    return render_template('mars.html', landing_image=image_url)