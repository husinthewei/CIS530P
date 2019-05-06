from datetime import datetime, date, timedelta
import json
import argparse
import random
import spacy
import os

import sys
sys.path.insert(0, 'code/extension-1')
sys.path.insert(0, 'code/extension-2')
sys.path.insert(0, 'code/extension-3')

from dateExtension import DateExtension
from datePatterns import find_date, match_date
from killedModelExtension import KilledModelExtension
from addressModelExtension import AddressModel

am = AddressModel()
km = KilledModelExtension(killed=True)
im = KilledModelExtension(killed=False)
dm = DateExtension()

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
    return km.predict_event(event)

# Returns random num from text or 0 if no nums
def pred_n_injured(event):
    return im.predict_event(event)

# Returns day before publish date
# or yesterday if no publish date
def pred_shooting_date(event):
    return dm.predict_event(event)

# Returns a random location
def pred_address(event, nlp):
    return am.predict_event(event)

def train(X_train, y_train):
    am.fit(X_train, y_train)
    dm.fit(X_train, y_train)
    km.fit(X_train, y_train)
    im.fit(X_train, y_train)

def predict(data):
    nlp = spacy.load("en_core_web_sm")

    predictions = []
    for event in data:
        event_pred = {}

        event_pred["n_killed"] = pred_n_killed(event)
        event_pred["n_injured"] = pred_n_injured(event)
        event_pred["shooting_date"] = pred_shooting_date(event)
        event_pred["address"] = pred_address(event, nlp)

        predictions.append(event_pred)

    return predictions

def run(dev):
    if dev:
        X_test = load(os.path.dirname(__file__) + '/../data/data-dev/X_val.json')
        X_train = load(os.path.dirname(__file__) + '/../data/data-train/X_train.json')
        y_train = load(os.path.dirname(__file__) + '/../data/data-train/y_train.json')
    else:
        X_test = load(os.path.dirname(__file__) + '/../data/data-test/X_test.json')
        X_train = load(os.path.dirname(__file__) + '/../data/data-train/X_train.json')
        y_train = load(os.path.dirname(__file__) + '/../data/data-train/y_train.json')

    train(X_train, y_train)
    pred = predict(X_test)

    return json.dumps(pred)

parser = argparse.ArgumentParser(description='Run the extensions.')
parser.add_argument("--dev", action='store_true', help="Run on dev dataset instead of test")
args = parser.parse_args()
print(run(args.dev))