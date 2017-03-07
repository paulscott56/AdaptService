
"""
Adapted from Adapt documentation at https://adapt.mycroft.ai/adapt/examples by seanfitz
"""

from flask import Flask, jsonify
from flask import request
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

app = Flask(__name__)

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()

# create and register weather vocabulary
cartype_keyword = [
    "rent",
    "transfer"
]

for ck in cartype_keyword:
    engine.register_entity(ck, "CarTypeKeyword")

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

for mo in months:
    engine.register_entity(mo, "MonthKeyword")

locations = [
    "Dublin",
    "Vienna",
    "Denver",
    "Cape Town",
    "Killarney"
]

for loc in locations:
    engine.register_entity(loc, "Location")

days = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"
]

for d in days:
    engine.register_entity(d, "DayKeyword")

# structure intent
car_intent = IntentBuilder("CarIntent")\
    .require("CarTypeKeyword")\
    .optionally("MonthKeyword")\
    .optionally("DayKeyword")\
    .require("Location")\
    .build()


for loc in locations:
    engine.register_entity(loc, "Location")


engine.register_intent_parser(car_intent)

@app.route('/', methods=['GET'])
def parseString():
    string = request.args.get('string')
    for intent in engine.determine_intent(string):
        print intent.get('confidence')
        if intent.get('confidence') > 0:
            return jsonify(intent)
        else:
            return 'intent not recognized'

    return 'failure'


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=False)
