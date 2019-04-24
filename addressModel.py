
import sklearn_crfsuite
import spacy

class AddressModel(object):
    def __init__(self):
        self.crf = sklearn_crfsuite.CRF( algorithm='lbfgs', c1=0.1, c2=0.1,max_iterations=100, all_possible_transitions=True)
        self.nlp = spacy.load("en_core_web_sm")
        self.desired_ents = ["FAC", "LOC"]


    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc]
        return sentences


    def __sent2features(self, sent):
        doc = self.nlp(sent)
        crime_terms = ["killed", "shot", "died"]
        features = {
            "crime_terms": sum([1 if w in crime_terms else 0 for w in doc.text]),
            "location": sum([1 if x.label_ in self.desired_ents else 0 for x in doc.ents])
        }
        return [features]

    def fit(self, X_event, y_event):
        y_train = []
        X_sents = []
        for event, label in zip(X_event, y_event):
            if label["address"] not in event["text"]: # discard any crap
                continue
            sents = self.__sent_tokenize(event["text"])
            X_sents.extend(sents)
            for sent in sents:
                if label["address"] in sent:
                    y_train.append(["CRL"])
                else:
                    y_train.append(["N-CRL"])

        X_train = [self.__sent2features(sent) for sent in X_sents]

        self.crf.fit(X_train, y_train)

    def predict_event(self, event):
        sents = self.__sent_tokenize(event["text"])
        X_test = [self.__sent2features(sent) for sent in sents]
        y_pred = self.crf.predict(X_test)
        for pred, sent in zip(y_pred, sents):
            if pred == "N-CRL": # no address here
                continue
            doc = self.nlp(sent)
            candidates = list(filter(lambda x: x.label_ in self.desired_ents, doc.ents))
            if len(candidates) != 0:
                return candidates[0].text
        
        # if the clf failed might as well go with simple-baseline
        # TODO
        return ""

    # def predict(self, X_events):
    #     return [self.__predict_event(event) for event in X_events]



    





