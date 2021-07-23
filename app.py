import flask
import requests
from flask import Flask, url_for, redirect, request
from flask import render_template
import requests
import os



app = Flask(__name__)
app.config["DEBUG"] = True
#It will hot-reload and automatically refresh our browser when a change in the code is detected

@app.route("/")
def show_landing_page():
    try: 
        return render_template("landing-page.html")
    except:
        return "An error occured."

@app.route("/search", methods=['POST'])
def form_submit():
    user_query = request.form['search_query'] # matches name attribute of query string input (HTML)
    redirect_url = url_for('.search_imdb', query_string=user_query)  # match search_imdb function name (Python flask)
    return redirect(redirect_url)


@app.route("/search/<query_string>", methods=["GET"])
def search_imdb(query_string):
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"

    querystring = {"q": query_string}
    key = os.getenv("x-rapidapi-key")
    host = os.getenv("x-rapidapi-host")
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': host
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()

        return render_template("search-result.html", data=data)
    except:
        return render_template("error404.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")