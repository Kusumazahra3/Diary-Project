from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

connection_string = "mongodb+srv://kusumazahra3:Juli2000@cluster0.yutp0ff.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    file_name = f'static/post-{mytime}.{extension}'
    file.save(file_name)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profile_name = f'static/profile-{mytime}.{extension}'
    profile.save(profile_name)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': file_name,
        'profile': profile_name,
        'title':title_receive,
        'content':content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)
    return jsonify({'msg':'Data was Saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)