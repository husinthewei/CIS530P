from simple-baseline import SimpleBaseline

def load(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def load_all():
    X_train = load('data/X_train.json')
    y_train = load('data/y_train.json')
    X_val = load('data/X_valjson')
    y_val = load('data/y_val.json')
    X_test = load('data/X_test.json')
    y_test = load('data/y_test.json')

def main():
    