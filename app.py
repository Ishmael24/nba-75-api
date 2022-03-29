from flask import Flask, jsonify
import pymongo
import json


app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["75-best-nba-players"]
players = mydb["players"]

def view_players():
    return list(mydb.players.find({}))

def view_pgs():
    return list(mydb.players.find({"position":"G"}))

@app.route("/")
def hello_world():
    #results = view_pgs()
    #results_json = json.dumps(results, default=lambda o: '<not serializable>')
    #print(results)
    return "results_json"