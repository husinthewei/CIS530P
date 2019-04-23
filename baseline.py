from datetime import datetime, date, timedelta
import json
import random
import spacy

from datePatterns import find_date, match_date

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
    text = event["text"]
    return pick_first_num_from_text(text)

# Returns random num from text or 0 if no nums
def pred_n_injured(event):
    text = event["text"]
    return pick_first_num_from_text(text)

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
    doc = nlp(event["text"])

    desired_ents = ["FAC", "LOC"]

    # Get words that are of the desired entities
    candidates = list(filter(lambda x: x.label_ in desired_ents, doc.ents))

    # Pick a random one
    pred = candidates[0].text if len(candidates) > 0 else ""
    
    return pred


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
    pred = predict(X_test)
    #with open('out.json', 'w') as f:
    #    f.write(json.dumps(pred))
    return json.dumps(pred)

print(run())