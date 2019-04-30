
import sklearn_crfsuite
import spacy
import sys
#from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.feature_extraction import DictVectorizer

class KilledModelExtension(object):
    def __init__(self, killed=True):
        self.crf = sklearn_crfsuite.CRF( algorithm='lbfgs', c1=0.1, c2=0.1,max_iterations=100, all_possible_transitions=True)
        self.model = SVC()#Perceptron()
        self.nlp = spacy.load("en_core_web_sm")
        injured_labels = ["O-INJ", "1-INJ", "2-INJ", "3-INJ", "4-INJ"]
        killed_labels = ["0-KILL", "1-KILL", "2-KILL", "3-KILL", "4-KILL"]
        self.field = "n_killed" if killed else "n_injured"
        self.arr_labels = killed_labels if killed else injured_labels
        self.killed =  killed
        self.vectorizer = DictVectorizer()

        #0.6585365853658537
        #0.17073170731707318 simple-baseline injured acc
        #0.3170731707317073  injured 
        #0.3170731707317073


    def __sent_tokenize(self, text):
        doc = self.nlp(text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences


    def __sent2features(self, sent, num):
        doc = self.nlp(sent)
        # print(doc.text, file=sys.stderr)
        death_terms = ["kill", "death", "die", "shot", "fatal"]
        injured_terms = ["hurt", "shot", "injured", "hospital", "wound"]

        features = {
            # "death_terms": sum([1 if w.lemma_ in death_terms else 0 for w in doc]),
            # "injured_terms": sum([1 if w.lemma_ in injured_terms else 0 for w in doc]),
            "int_number": int(num) if num.isdigit() else 0,
            "str_number": num if not num.isdigit() else "",
            "n_people": len([ent for ent in doc.ents if ent.label_ == "PERSON"])
        }
        return features

    def assign_label(self, num):
        arr = self.arr_labels
        idx = len(arr) - 1 if num > len(arr) - 1 else num
        return self.arr_labels[idx]

    def __cardinal2number(self, card):
        num = card.lower()
        d = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
        if num in d:
            return d[num]
        else:
            return -1


    def __doc2features(self, doc):
        death_terms = ["kill", "death", "die", "fatal", "killed"]
        injured_terms = ["hurt", "shot", "injured", "hospital", "wound", "wounded"]
        roads = ["Rd", "St", "Ave", "Blvd", "Ln", "Dr", "Ter", "Pl", "Ct"]

        int_num = 0
        str_num = ""

        for ent in doc.ents:
            if ent.label_ == "CARDINAL":
                num = ent.text
                if num.isdigit():
                    int_num = int(num)
                else:
                    str_num = num

        unique_people = []

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                p = ent.text
                if len(p.split()) > 0:
                    lastname = p.split()[-1]
                    if lastname in roads:
                        continue
                    unique_people.append(lastname)
                else:
                    unique_people.append(p)

        unique_people = set(unique_people)



        # features = {
        #     # "death_terms": sum([1 if w.lemma_ in death_terms else 0 for w in doc]),
        #     # "injured_terms": sum([1 if w.lemma_ in injured_terms else 0 for w in doc]),
        #     # "int_number": int(num) if num.isdigit() else 0,
        #     # "str_number": num if not num.isdigit() else "",
        #     # "int_number": int_num,
        #     # "str_number": str_num,
        #     "n_people": len(unique_people),
        #     "n_killed_terms:" sum([1 if w.text in death_terms else 0 for w in doc]) 
        # }
        features = [
            len(unique_people),
            sum([1 if w.text in death_terms else 0 for w in doc]),
            sum([1 if w.text in injured_terms else 0 for w in doc]),
        ]


        return features

    def fit(self, X_event, y_event):
        y_train = []
        X_train = []
        for event, label in zip(X_event, y_event):
            doc = self.nlp(event["text"])
            sub_label = []
            # sub_train = []

            sub_train = self.__doc2features(doc)
            # for span in doc.sents:
            #     for token in span:
            #         if token.pos_ == "NUM":
            #             al = self.assign_label(label[self.field])
            #             sub_label.append(al)
            #             sub_train.append(self.__sent2features(span.string.strip(), token.text))
            #             break
            #     else:
            #         sub_label.append(self.arr_labels[0])
            #         sub_train.append(self.__sent2features(span.string.strip(), "0"))


            #print(sub_train)
            y_train.append(label[self.field])
            X_train.append(sub_train)


        #X_train = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_train, y_train)

    def predict_event(self, event):
        doc = self.nlp(event["text"])



        # sub_train = []
        # for span in doc.sents:
        #     for token in span:
        #         if token.pos_ == "NUM":
        #             sub_train.append(self.__sent2features(span.string.strip(), token.text))
        #             break
        #     else:
        #         sub_train.append(self.__sent2features(span.string.strip(), "0"))

        sub_train = self.__doc2features(doc)

        X_test = [sub_train]


        #X_test = self.vectorizer.transform(X_test)

        y_pred = self.model.predict(X_test)

        #n_killed = [self.arr_labels.index(label) for label in y_pred]
        return int(y_pred[0])

    # def predict(self, X_events):
    #     return [self.__predict_event(event) for event in X_events]



    





