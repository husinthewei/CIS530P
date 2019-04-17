import json
from sklearn.model_selection import train_test_split


def write_json_to_file(filename, json_obj):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_obj))

def main():
    # read and load data
    data = {}
    with open('530_test_data.json', 'r') as f:
        data = json.loads(f.read())

    # split data into X and y
    X = []
    y = []
    for event in data:
        ydict = {
            "n_killed": event["n_killed"],
            "n_injured": event["n_injured"],
            "shooting_date": event["shooting_date"],
            "address": event["address"]
        }
        X.append(event["text"])
        y.append(ydict)

    # split X and y into training 70%, validation 9%, test 21%
    X_train, X_inter, y_train, y_inter = train_test_split(X, y, test_size=0.3)
    X_val, X_test, y_val, y_test = train_test_split(X_inter, y_inter, test_size=0.7)

    # output split to json file
    write_json_to_file('X_train.json', X_train)
    write_json_to_file('X_val.json',   X_val)
    write_json_to_file('X_test.json',  X_test)
    write_json_to_file('y_train.json', y_train)
    write_json_to_file('y_val.json',   y_val)
    write_json_to_file('y_test.json',  y_test)



if __name__ == "__main__":
    main()