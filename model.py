
# Default model. All models should subclass from this.
class Model(object):

    def fit(X_train):
        pass
    
    def predict(X):
        predictions = []
        for event in X:
            event_pred = {}

            event_pred["n_killed"] = ""
            event_pred["n_injured"] = ""
            event_pred["shooting_date"] = ""
            event_pred["address"] = ""

            predictions.append(event_pred)

        return predictions
