##Mood-based music generator project

#importing all the important stuff
from flask import Flask, request, render_template, redirect, url_for
import json
import pandas as pd
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)
df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\all_songs2.csv", encoding="ISO-8859-1")

user_data = {}

#the first page
@app.route('/', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form.get('name')
        playlist_name = request.form.get('playlist_name')
        user_data['name'] = name
        user_data['playlist_name'] = playlist_name
        return redirect(url_for('select_genre'))
    return render_template('enter_name.html')

#the second page
@app.route('/select_genre', methods=['GET', 'POST'])
def select_genre():
    global db
    user_name = user_data.get('name')
    playlist_name = user_data.get('playlist_name')
    if not user_name:
        return redirect(url_for('enter_name'))
    db = None
    if request.method == 'POST':
        selected_genre = request.form.get("choice")
        lower_happiness = request.form.get('happinessLower')
        upper_happiness = request.form.get('happinessUpper')
        lower_energized = request.form.get('energizedLower')
        upper_energized = request.form.get('energizedUpper')
        genre_conditions = {
            "pop": ['Rock', 'Country', 'Country, Rock', 'Rock, Country', 'House', 'House, Rock', 'Rock, House'],
            "rock": ['Pop', 'Country', 'Country, Pop', 'Pop, Country', 'House', 'House, Pop', 'Pop, House'],
            "country": ['Pop', 'Rock', 'Rock, Pop', 'Pop, Rock', 'House', 'House, Rock', 'Rock, House', 'House, Pop', 'Pop, House'],
            "house": ['Pop', 'Rock', 'Rock, Pop', 'Pop, Rock', 'Country', 'Country, Rock', 'Rock, Country', 'Country, Pop', 'Pop, Country']
        }
        invalid_genres = genre_conditions.get(selected_genre, [])
        db = df.loc[
            (df['Happy'].between(float(lower_happiness), float(upper_happiness))) &
            (df['Energy'].between(float(lower_energized), float(upper_energized))) &
            (~df['Parent-Genres'].isin(invalid_genres))
        ]
        if db.empty:
            return "No matching songs found."
        return redirect(url_for('display_results'))
    return render_template('select_genre.html', name=user_name)

#the final page
@app.route('/results', methods=['GET', 'POST'])
def display_results():
    user_name = user_data.get('name')
    selected_genre = request.form.get("choice")
    playlist_name = user_data.get('playlist_name')
    if not user_name:
        return redirect(url_for('enter_name'))
    if db is not None:
        json_data = db.to_json(orient='records', default_handler=str)
        html_data = db.to_html(classes='table table-striped', escape=False)
        return render_template("results.html", result_df=db, genre_choice=selected_genre, data=html_data, json_data=json_data, user_data=user_data)
    else:
        return "No data available. Please select a genre first."

#code to generate the playlist in spotify once button on the results page is pressed
@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    user_name = user_data.get('name')
    playlist_name = user_data.get('playlist_name')
    if not user_name:
        return redirect(url_for('enter_name'))
    if db is not None:
        json_data = db.to_json(orient='records', default_handler=str)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='383e49d4b1bb4a0693c98440482c3210',
            client_secret='0f90919a8f8343fd884bbad4ee27e20f',
            redirect_uri='http://localhost/',
            scope='playlist-modify-public'
        ))
        username = 'svea.boesch'
        playlist = sp.user_playlist_create(username, playlist_name, public=True)
        parsed_json_data = json.loads(json_data)
        song_uris = [item["Spotify-Track-Id"] for item in parsed_json_data]
        sp.playlist_add_items(playlist['id'], song_uris)        
        return redirect(url_for('display_results', json_data=json_data))
    else:
        return "No data available. Please select a genre first."

if __name__ == "__main__":
    app.run(debug=True)