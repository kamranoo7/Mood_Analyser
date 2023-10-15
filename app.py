from flask import Flask, render_template, request, redirect, url_for,flash
import openai

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os

#  your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

#Home Route

@app.route('/')
def home():
    return render_template('home.html')
#Signup Page Route
@app.route('/signup')
def signup():
    return render_template('signup.html')
#Login Page Route
@app.route('/login')
def login():
    return render_template('login.html')
#Index Page Route
@app.route('/index')
def lindex():
    return render_template('index.html')

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        mood = analyze_mood(text)
        if "An error occurred" in mood:
            flash(mood, "error")
            return redirect(url_for("index"))
        return render_template("result.html", mood=mood)

    return render_template("index.html")
#Mood Analyzing
def analyze_mood(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes mood."},
            {"role": "user", "content": text},
        ],
    )
    sentiment = response.choices[0].message["content"].strip().lower()


    if "positive" in sentiment:
        return "Positive Mood"
    elif "negative" in sentiment:
        return "Negative Mood"
    else:
        return "Neutral Mood"

if __name__ == "__main__":
    app.run(debug=True)

