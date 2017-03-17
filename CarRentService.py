
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
from datetime import datetime
from datetime import timedelta
import urllib2

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
    "Killarney",
    "Munich"
]

loccodes = {"Munich" : 626, "Dublin" : 1370, "Vienna" : 2225, "Denver" : 1869, "Cape Town": 1674, "Killarney" : 1366}

for loc in locations:
    engine.register_entity(loc, "Location")

days = [
    "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"
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
        if intent.get('confidence') > 0:
            # Get the location code from the parsed intent
            locationKeyword = intent["Location"]
            loccode = loccodes[locationKeyword]

            # get the dates
            year = 2017
            daynum = intent["DayKeyword"][:-2]
            month = intent["MonthKeyword"]
            fromdatestr = str(daynum) + "/" + month + "/" + str(year)
            fromdate = datetime.strptime(fromdatestr, '%d/%B/%Y')
            fdate = fromdate.strftime('%d/%B/%Y')
            todate = fromdate + timedelta(days=5)
            tdate = todate.strftime('%d/%B/%Y')
            # we assume a 5 day long rental, because I said so...
            url = 'https://api.mobacartest.com/v1/1/quotes?searchCurrency=GBP&age=44&countryResISO=GB&dateFrom=' + fdate + '&dateTo=' + tdate + '&TimeFrom=10:00&TimeTo=10:00&pickupLocID=' + str(loccode) + '&dropoffLocID=' + str(loccode)
            quotes =  urllib2.urlopen(url).read()
            return quotes #jsonify(intent)
        else:
            return 'intent not recognized'

    return 'failure'


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=False)
