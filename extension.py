from datetime import datetime, date, timedelta
import json
import random
import spacy


from datePatterns import find_date, match_date
from addressModel2 import AddressModel2
from killedModelExtension import KilledModelExtension
from dateExtension import DateExtension

am = AddressModel2()
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
    return km.predict_event(event)#0#pick_first_num_from_text(text)

# Returns random num from text or 0 if no nums
def pred_n_injured(event):
    return im.predict_event(event)

# Returns day before publish date
# or yesterday if no publish date
def pred_shooting_date(event):
    return dm.predict_event(event)

# Returns a random location
def pred_address(event, nlp):
    
    return ""#am.predict_event(event)

def train(X_train, y_train):
    #am.fit(X_train, y_train)
    dm.fit(X_train, y_train)
    km.fit(X_train, y_train)
    im.fit(X_train, y_train)
    #pass


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
    X_test = load('data/X_test.json')
    X_train = load('data/X_val.json')
    y_train = load('data/y_val.json')

    train(X_train, y_train)
    pred = predict(X_test)
    #with open('out.json', 'w') as f:
    #    f.write(json.dumps(pred))
    return json.dumps(pred)

print(run())