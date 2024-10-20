from flask import Flask, render_template, request, redirect, jsonify
from main import TimeMachine
import webbrowser

app = Flask(__name__)
tm = TimeMachine()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_y = request.form["year"]
    loaded_playlists = tm.load_json()
    if input_y in loaded_playlists:
        print(loaded_playlists)
        link = loaded_playlists[input_y]
        return redirect(link)
    else:
        link = tm.give_playlist(int(input_y))
        loaded_playlists[input_y] = link
        tm.save_json(loaded_playlists)
        return redirect(link)



if __name__ == '__main__':
    app.run(debug=True)


