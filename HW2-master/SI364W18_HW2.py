## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album_name = StringField('Enter the name of an album: ', [Required])
    album_rating = RadioField("How much do you like this album? (1 low, 3 high)", [Required], choices=[('1', '1'), ('2', '2'), ('3', '3')])
    submit = SubmitField("Submit")

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform', methods = ['GET'])
def artistformfunc():
    return render_template("artistform.html")

@app.route('/artistinfo', methods = ['GET'])
def artistinfofunc():
    base_url = "https://itunes.apple.com/search?term=" + request.args.get("artist")
    req = requests.get(base_url)
    json_data = json.loads(req.text)
    return render_template("artist_info.html", objects=json_data['results'])

@app.route('/artistlinks')
def artistlinks():
    return render_template(artist_links)

@app.route('/specific/song/<artist_name>')
def specificSong(artist_name):
    base_url = "https://itunes.apple.com/search?term=" + artist_name
    req = requests.get(base_url)
    json_data = json.loads(req.text)
    response = json_data['results']
    return render_template("specific_artist.html", results=response)

@app.route('/album_entry', methods = ['GET'])
def albumEntry():
    if request.method == "GET":
        form = AlbumEntryForm()
        return render_template('album_entry.html', form=form)

@app.route('/album_result', methods = ['GET'])
def album_result():
    if request.method == "GET":
        albumt_title = request.args.get('album_name')
        rating  = request.args.get('album_rating')
        list_info = [albumt_title, rating]
        return render_template('album_data.html', results = list_info)


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
