from flask import Flask, render_template, request, redirect, url_for
import requests
import os

api_key = os.environ.get('API_KEY')

app = Flask(__name__)

@app.route('/')
def index():

    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")

    response = response.json()
    url = response['url']

    image_title = response['title']
    image_explanation = response['explanation']
    image_date = response['date']

    return render_template('index.html', landing_image=url, image_title=image_title, image_explanation=image_explanation, image_date=image_date)

@app.route('/mars', methods=['GET','POST'])
def mars():


    if request.form.get('selected') == None:
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=mast&api_key={api_key}')
    else:
        camera = request.form.get('selected')
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera={camera}&api_key={api_key}')

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