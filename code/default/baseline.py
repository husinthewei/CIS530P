from datetime import datetime, date, timedelta
import os
import json
import random
import spacy

from datePatterns import find_date, match_date
from addressModel import AddressModel
from killedModel import KilledModel

am = AddressModel()
km = KilledModel(killed=True)
im = KilledModel(killed=False)

def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

# Returns 0 if no numbers in text
def pick_first_num_from_text(text):
    nums = [int(s) for s in text.split() if s.isdigit()]
    return nums[0] if len(nums) > 0 else 0

# Returns random num from text or 0 if no nums
def pred_n_killed(event):
    return km.predict_event(event)#0#pick_first_num_from_text(text)

# Returns random num from text or 0 if no nums
def pred_n_injured(event):
    return im.predict_event(event)

# Returns day before publish date
# or yesterday if no publish date
def pred_shooting_date(event):
    if event['publish_date'] == "":
        pred_event_date = match_date(event['text'])
    else:
        pred_event_date = find_date(event['text'], event['publish_date'])

    if pred_event_date is None:
        pred_event_date = datetime.strptime(event['publish_date'], "%Y-%m-%d")

    return pred_event_date.strftime("%Y-%m-%d")

# Returns a random location
def pred_address(event, nlp):
    
    return am.predict_event(event)

def train(X_train, y_train):
    am.fit(X_train, y_train)
    km.fit(X_train, y_train)
    im.fit(X_train, y_train)


def predict(data):
    nlp = spacy.load("en_core_web_sm")

    predictions = []
    for event in data:
        event_pred = {}

        #event_pred["incident_id"] = event["incident_id"]
        event_pred["n_killed"] = pred_n_killed(event)
        event_pred["n_injured"] = pred_n_injured(event)
        event_pred["shooting_date"] = pred_shooting_date(event)
        event_pred["address"] = pred_address(event, nlp)

        predictions.append(event_pred)

    return predictions

def run():
    X_test = load(os.path.dirname(__file__) + '/../../data/data-test/X_test.json')
    X_train = load(os.path.dirname(__file__) + '/../../data/data-train/X_train.json')
    y_train = load(os.path.dirname(__file__) + '/../../data/data-train/y_train.json')

    train(X_train, y_train)
    pred = predict(X_test)

    return json.dumps(pred)

print(run())