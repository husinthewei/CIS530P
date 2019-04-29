

from sklearn.linear_model import LogisticRegression
from datePatterns import find_date_ft
import spacy

class DateExtension(object):
    def __init__(self):
        self.clf = LogisticRegression()
        self.nlp = spacy.load("en_core_web_sm")


    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences


    def __sent2features(self, sent, ft):
        doc = sent.split()
        crime_terms = ["killed", "shot", "died", "shooting"]
        #police_terms = ["Police", "Department"]
        court_terms = ["court", "Court", "Courthouse", "prison", "trial", "sentenced", "sentencing"]
        misleading_terms = ["Published"]
        features = [
            sum([1 if w in crime_terms else 0 for w in doc]),
            sum([1 if w in court_terms else 0 for w in doc]),
            sum([1 if w in misleading_terms else 0 for w in doc]),
            ft
        ]
        return features

    def fit(self, X_event, y_event):
        X_train = []
        y_train = []
        X_event = X_event[0:1000]
        y_event = y_event[0:1000]
        count = 0
        for event, label in zip(X_event, y_event):
            sents = self.__sent_tokenize(event["text"])
            #X_sents.extend(sents)
            for sent in sents:
                pred_date, ft = find_date_ft(sent, event["publish_date"])
                if pred_date is not None:
                    X_train.append(self.__sent2features(sent, ft))
                    if pred_date.strftime("%Y-%m-%d")== label["shooting_date"]:
                        y_train.append(1)
                    else:
                        y_train.append(0)
            count += 1
            #if count % 100 == 0:
                #print(str(count/10) + " percent training")

        #print(X_train)

        self.clf.fit(X_train, y_train)

    def predict_event(self, event):
        sents = self.__sent_tokenize(event["text"])
        X_dates = []
        X_test = []
        for sent in sents:
            pred_date, ft = find_date_ft(sent, event["publish_date"])
            if pred_date is not None:
                X_test.append(self.__sent2features(sent, ft))
                X_dates.append(pred_date.strftime("%Y-%m-%d"))

        y_pred = self.clf.predict(X_test)
        #print(self.clf.predict_proba(X_test))
        for pred, candidate_date in zip(y_pred, X_dates):
            if pred == 1:
                return candidate_date

        if len(X_dates) > 0:
            return X_dates[0]

        return event["publish_date"]

    # def predict(self, X_events):
    #     return [self.__predict_event(event) for event in X_events]



    





