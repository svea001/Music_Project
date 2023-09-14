from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import logging
import csv


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


df = None
happiness_lower = happiness_upper = energized_lower = energized_upper = None
artist_choice = None


@app.route('/some_route', methods=['GET', 'POST'])
def some_route():
    app.logger.debug("Entering some_route")
    return render_template('template.html')

@app.route('/', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('select_artist', name=name))
    return render_template('enter_name.html')


@app.route('/select_artist/<name>', methods=['GET', 'POST'])
def select_artist(name):
    global df, artist_choice
    if request.method == 'POST':
        choice = request.form.get("choice")
        artist_choice = choice 
        app.logger.debug(f"Selected artist choice: {choice}")
        if choice == "all":
            csv_file_path = r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\all_songs3.csv"
            print(f"CSV File Path: {csv_file_path}")  # Debug print
            try:
                df = pd.read_csv(csv_file_path, sep='\t', encoding='utf-8')
                # Strip whitespace from column names
                df.columns = df.columns.str.strip()
                # Strip whitespace from 'Energy' and 'Happy' columns if needed
                df['Energy'] = df['Energy'].str.strip()
                df['Happy'] = df['Happy'].str.strip()
                print(df)  # Debug print to show the loaded DataFrame
            except Exception as e:
                print(f"Error reading CSV: {str(e)}")
        elif choice == "taylor_swift":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\tsapi_songs.csv")
        elif choice == "the_cure":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\cure_songs.csv")
        elif choice == "kip_moore":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\kip_moore_songs.csv")
        elif choice == "lana_del_rey":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\lana_songs.csv")
        elif choice == "luke_bryan":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\luke_bryan_songs.csv")
        elif choice == "arctic_monkeys":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\monkeys_songs.csv")
        elif choice == "stevie_nicks":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\stevie_nicks_songs.csv")
        elif choice == "mitski":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\mitski_songs.csv")
        elif choice == "zac_brown":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\zac_brown_songs.csv")
        elif choice == "ac_dc":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\acdc_songs.csv")
        elif choice == "the_beatles":
            df = pd.read_csv(r"C:\Users\sveab\Downloads\MUSIC_PROJECT\Database\beatles_songs.csv")
        return redirect(url_for('display_results', name=name, artist_choice=choice))
    return render_template('select_artist.html', name=name)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    global df, happiness_lower, happiness_upper, energized_lower, energized_upper
    if request.method == 'POST':
        name = request.form.get('name')
        happiness_lower = int(request.form['happiness-lower'])
        happiness_upper = int(request.form['happiness-upper'])
        energized_lower = int(request.form['energized-lower'])
        energized_upper = int(request.form['energized-upper'])
        print(happiness_upper)
        return redirect(url_for('display_results', name=name, artist_choice=artist_choice))
    return redirect(url_for('select_artist', name=name))

@app.route('/results', methods=['GET', 'POST'])
def display_results():
    global df, artist_choice, happiness_lower, happiness_upper, energized_lower, energized_upper
    app.logger.debug(f"Display Results: df={df}")
    print(df)
    if df is not None:
        #Debug
        app.logger.debug(f"Happy lower={happiness_lower}, Happy upper={happiness_upper}")
        app.logger.debug(f"Energy lower={energized_lower}, Energy upper={energized_upper}")
        app.logger.debug(f"Loaded DataFrame: {df}")
        app.logger.debug(f"Data types - Happy: {df['Happy'].dtype}, Energy: {df['Energy'].dtype}")        
        app.logger.debug(f"Happy Range: {df['Happy'].min()} - {df['Happy'].max()}")
        app.logger.debug(f"Energy Range: {df['Energy'].min()} - {df['Energy'].max()}")
        
        #Checking
        print(energized_lower)
        print(energized_upper)
        print(happiness_lower)
        print(happiness_upper)

        # Apply the condition to filter rows based on 'Happy' column
        filtered_df_happy = df[df['Happy'] >= happiness_lower]
        
        app.logger.debug(f"Filtered DataFrame (Happy Filter): {filtered_df_happy}")
        
        # Now, filter based on 'Energy' column using the previous result
        result_df = filtered_df_happy[filtered_df_happy['Energy'].between(energized_lower, energized_upper)]
        
        app.logger.debug(f"Result DataFrame: {result_df}")
        
        return render_template("results.html", result_df=result_df, artist_choice=artist_choice)
    else:
        return "No data available. Please select an artist first."



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
