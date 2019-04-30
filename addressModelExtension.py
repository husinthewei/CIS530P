import sklearn_crfsuite
import spacy
import re

class AddressModel2(object):
    def __init__(self):
        self.crf = sklearn_crfsuite.CRF( algorithm='lbfgs', c1=0.1, c2=0.1,max_iterations=100, all_possible_transitions=True)
        self.nlp = spacy.load("en_core_web_sm")
        self.desired_ents = ["FAC", "LOC"]
        
        self.death_terms = ["killed", "death", "died", "shot", "fatal"]
        self.injured_terms = ["hurt", "shot", "injured", "hospitalized", "wounded"]

        roads = ["Rd", "St", "Ave", "Blvd", "Ln", "Dr", "Ter", "Pl", "Ct"]

        addr_regex1 = r"[0-9]* block of( [^ ]*){1,2} (" + "|".join(roads) + ")"
        addr_regex2 = r"[0-9]+( [^ ]*){1,2} (" + "|".join(roads) + ")"
        addr_regex3 = r"([^ ]* ){1,2}(" + "|".join(roads) + ") and( [^ ]*){1,2} (" + "|".join(roads) + ")"
        self.addr_regex = "(" + addr_regex1 + "|" + addr_regex2 + "|" + addr_regex3 + ")"

    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc]
        return sentences


    # loc is 1 if sentence contains at least 1 location
    # 0 otherwise
    def __sent2features(self, sent, loc):
        doc = self.nlp(sent)

        features = {
            "death_terms": sum([1 if w.text in self.death_terms else 0 for w in doc]),
            "injured_terms": sum([1 if w.text in self.injured_terms else 0 for w in doc]),
            "location": loc,
            "contains_addr": 1 if re.search(self.addr_regex, doc.text) else 0
        }
        return features

    def assign_label(self, num):
        arr = self.arr_labels
        idx = len(arr) - 1 if num > len(arr) - 1 else num
        return self.arr_labels[idx]

    def fit(self, X_event, y_event):
        y_train = []
        X_train = []
        for event, label in zip(X_event, y_event):
            doc = self.nlp(event["text"])
            sub_label = []
            sub_train = []
            for span in doc.sents:
                sub_label.append("CRL" if label["address"] in span.string and label["address"] != "" else "N-CRL")
                
                for token in span:
                    if token.ent_type_ in self.desired_ents:
                        sub_train.append(self.__sent2features(span.string.strip(), 1))
                        break
                else:
                    sub_train.append(self.__sent2features(span.string.strip(), 0))

            y_train.append(sub_label)
            X_train.append(sub_train)

        self.crf.fit(X_train, y_train)

    def predict_event(self, event):
        doc = self.nlp(event["text"])
        sub_train = []
        for span in doc.sents:
            for token in span:
                if token.ent_type_ in self.desired_ents:
                    sub_train.append(self.__sent2features(span.string.strip(), 1))
                    break
            else:
                sub_train.append(self.__sent2features(span.string.strip(), 0))

        X_test = [sub_train]

        y_pred = self.crf.predict(X_test)
        for pred, span in zip(y_pred[0], doc.sents):
            if pred == "N-CRL": # no address here
                continue

            candidates = list(filter(lambda x: x.label_ in self.desired_ents, span.ents))
            addr = re.search(self.addr_regex, event["text"])

            if addr:
                return addr.group(0)
            elif len(candidates) != 0:
                return candidates[0].text
        return ""