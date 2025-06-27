from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from ai_utils.granite_response import get_granite_response
from ai_utils.sentiment import analyze_sentiment
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient(os.getenv("MONGO_URI"))
db = client['citizen_ai']
chat_collection = db['chats']
sentiment_collection = db['sentiments']
concern_collection = db['concerns']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response = None
    show_feedback = False

    if request.method == 'POST':
        if 'question' in request.form:
            question = request.form.get('question')
            response = get_granite_response(question)
            chat_collection.insert_one({'question': question, 'response': response})
            show_feedback = True

    return render_template("chat.html", latest=response, show_feedback=show_feedback)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = request.form.get('feedback')
    sentiment = analyze_sentiment(feedback)
    sentiment_collection.insert_one({'feedback': feedback, 'sentiment': sentiment})
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    sentiments = list(sentiment_collection.find({}, {'_id': 0}))
    pos = sum(1 for s in sentiments if s['sentiment'] == "Positive")
    neu = sum(1 for s in sentiments if s['sentiment'] == "Neutral")
    neg = sum(1 for s in sentiments if s['sentiment'] == "Negative")
    concerns = list(concern_collection.find({}, {'_id': 0}))
    return render_template("dashboard.html", pos=pos, neu=neu, neg=neg, concerns=concerns)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ✅ Accept ANY username/password
        session['logged_in'] = True
        return redirect(url_for('chat'))  # Send them straight to chat
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
