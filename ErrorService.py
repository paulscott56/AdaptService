
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
error_keyword = [
    "error",
    "e",
    "E"
]

for er in error_keyword:
    engine.register_entity(er, "ErrorKeyword")

error_types = [
    "E16",
    "E17",
    "E19",
    "E30"
    
]

for et in error_types:
    engine.register_entity(et, "ErrorType")

# create regex to parse out locations
#engine.register_regex_entity("in (?P<Location>.*)")

# structure intent
error_intent = IntentBuilder("ErrorIntent")\
    .require("ErrorKeyword")\
    .optionally("ErrorType")\
    .build()

engine.register_intent_parser(error_intent)

@app.route('/', methods=['GET'])
def parseString():
    string = request.args.get('string')
    for intent in engine.determine_intent(string):
        if intent.get('confidence') > 0:
            print intent.get("ErrorType")
            if intent.get("ErrorType") == "E16":
                return jsonify({"msg":"Transmission might be temporarily suspended. Press MENU on your remote control, then 4 to check your Mail Messages. If you have a notification from us to pay your account, then payment needs to be made before services can be reactivated. If your account is not suspended, then SMS E16 followed by your Smartcard number to 32472 or visit My DStv to clear the error code."})
            elif intent.get("ErrorType") == "E17":
                return jsonify({"msg":"Ensure Smartcard is inserted in the decoder and either: SMS E17 + Smartcard number to 32472 Reset the service yourself by logging into My DStv and fix errors. Use the Voice Self Help option through your local DStv Call Centre."})
            elif intent.get("ErrorType") == "E19":
                return jsonify({"msg":"Please wait a few minutes for your subscription status to be verified. Please contact your nearest DStv Call Centre if the message is not cleared in two minutes."})
            elif intent.get("ErrorType") == "E30":
                return jsonify({"msg":"Please check that the cables from the satellite dish are securely connected to the correct inputs on the back of the decoder. Then switch the decoder off at the  plug, wait 10 seconds, and switch it back on again. If this error is not cleared, visit Self Service on www.dstv.com for troubleshooting steps or contact the DStv Call Centre."})
            #return jsonify(intent)
        else:
            return 'intent not recognized'

    return 'failure'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
