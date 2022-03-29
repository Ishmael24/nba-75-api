from flask import Flask, jsonify
import pymongo
import json
from bson.json_util import dumps

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
    results = view_pgs()
    results_list = list(results)
    #print(results)
    return dumps(results_list)