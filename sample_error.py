import json
import argparse
import warnings 
from sklearn.metrics import f1_score, precision_score, recall_score

parser = argparse.ArgumentParser()

parser.add_argument('--goldfile', type=str, required=True)
parser.add_argument('--predfile', type=str, required=True)
parser.add_argument('--inputfile', type=str, required=True)
parser.add_argument('--limit', type=int, default=2)
parser.add_argument('--field', type=str, default='shooting_date')

star_str = "*************************************************" * 2
dash_str = "-------------------------------------------------" * 2


def read_labels(file):
    with open(file) as f:
        incidents = json.load(f)

    return incidents


def main(args):
    gold = read_labels(args.goldfile)
    pred = read_labels(args.predfile)
    text = read_labels(args.inputfile)

    count = 0
    for i in range(len(gold)):
        if gold[i][args.field] != pred[i][args.field]:
            print()
            print(dash_str)
            print(star_str)
            print("Actual: {}   Expected: {} \t Date-published: {}   Index#: {}".format(pred[i][args.field], gold[i][args.field], text[i]["publish_date"], i))
            print(dash_str)
            print(text[i]["text"])
            print()
            count += 1
        if count == args.limit:
            break



if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

