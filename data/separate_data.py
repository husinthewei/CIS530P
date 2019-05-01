import json
from sklearn.model_selection import train_test_split
import argparse

defaultfiles = ["raw/gv_data_1.json", "raw/gv_data_2.json", "raw/gv_data_3.json", "raw/gv_data_4.json", "raw/gv_data_5.json", "raw/gv_data_6.json", "raw/gv_data_7.json", "raw/gv_data_235.json", "raw/gv_data_236.json", "raw/gv_data_237.json", "raw/gv_data_238.json", "raw/gv_data_239.json", "raw/gv_data_240.json"]

road_map = {"Road": "Rd", "Street": "St", "Avenue": "Ave", "Boulevard": "Blvd", 
            "Lane": "Ln", "Drive": "Dr", "Terrace": "Ter", "Place": "Pl", "Court": "Ct",
            "Roads": "Rd", "Streets": "St", "Avenues": "Ave", "Boulevards": "Blvd", 
            "Lanes": "Ln", "Drives": "Dr", "Terraces": "Ter", "Places": "Pl", "Courts": "Ct",
            "road": "Rd", "street": "St", "avenue": "Ave", "boulevard": "Blvd", 
            "lane": "Ln", "drive": "Dr", "terrace": "Ter", "place": "Pl", "court": "Ct"}

road_map_inv = {"Rd": "Road", "St": "Street", "Ave": "Avenue", "Blvd": "Boulevard", "Ln": "Lane", "Dr": "Drive", "Ter": "Terrace", "Pl": "Place", "Ct": "Court", "Cir": "Circle", "Rd.": "Road", "St.": "Street", "Ave.": "Avenue", "Blvd.": "Boulevard", "Ln.": "Lane", "Dr.": "Drive", "Ter.": "Terrace", "Pl.": "Place", "Ct.": "Court", "Cir.": "Circle"}

parser = argparse.ArgumentParser()
parser.add_argument('--jsonfiles', type=str, nargs='+', default=defaultfiles)


def write_json_to_file(filename, json_obj):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_obj))


def clean_addresses(text, remove_punc = False):
    if remove_punc:
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace(";", "")
    address_cleaned = [road_map_inv[tok] if tok in road_map_inv else tok 
                       for tok in text.split()]
    return " ".join(address_cleaned)

def main(args):
    # read and load data
    data = []


    for filename in args.jsonfiles:
        with open(filename) as f:
            data = data + json.loads(f.read())

    # split data into X and y
    X = []
    y = []
    for event in data:

        event["text"] = clean_addresses(event["text"])
        event["address"] = clean_addresses(event["address"], remove_punc = True)

        # skip all faulty articles
        if event["publish_date"] == "" or event["address"] not in event["text"]:
            continue

        if event["shooting_date"] > event["publish_date"]:
            continue

        xdict = {
            "text": event["text"],
            "publish_date": event["publish_date"]
        }

        ydict = {
            "n_killed": event["n_killed"],
            "n_injured": event["n_injured"],
            "shooting_date": event["shooting_date"],
            "address": event["address"]
        }

        X.append(xdict)
        y.append(ydict)

    print(len(X))

    # split X and y into training 70%, validation 9%, test 21%
    X_train, X_inter, y_train, y_inter = train_test_split(X, y, test_size=0.10, random_state=16)
    X_val, X_test, y_val, y_test = train_test_split(X_inter, y_inter, test_size=0.5, random_state=42)
    #print(len(X_train))
    #print(len(X_val))
    #print(len(X_test))

    # output split to json file
    write_json_to_file('X_train.json', X_train)
    write_json_to_file('X_val.json',   X_val)
    write_json_to_file('X_test.json',  X_test)
    write_json_to_file('y_train.json', y_train)
    write_json_to_file('y_val.json',   y_val)
    write_json_to_file('y_test.json',  y_test)



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)