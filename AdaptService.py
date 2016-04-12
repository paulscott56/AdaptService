
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
weather_keyword = [
    "weather"
]

for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword")

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    engine.register_entity(wt, "WeatherType")

# create regex to parse out locations
engine.register_regex_entity("in (?P<Location>.*)")

# structure intent
weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()

engine.register_intent_parser(weather_intent)

@app.route('/', methods=['GET'])
def parseString():
    string = request.args.get('string')
    for intent in engine.determine_intent(string):
        if intent.get('confidence') > 0:
            return jsonify(intent)
        else:
            return 'intent not recognized'

    return 'failure'


if __name__ == '__main__':
    app.run(debug=True)