import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--goldfile', type=str, required=True)
parser.add_argument('--predfile', type=str, required=True)


def read_labels(file):
    with open(file) as f:
        incidents = json.load(f)

    return incidents


def compute_acc(gold, pred, field):
    num_correct = 0
    for i in range(len(gold)):
        if gold[i][field] == pred[i][field]:
            num_correct += 1

    return num_correct / len(gold)



def main(args):
    gold = read_labels(args.goldfile)
    pred = read_labels(args.predfile)

    addr_acc = compute_acc(gold, pred, "address")
    date_acc = compute_acc(gold, pred, "shooting_date")
    n_killed_acc = compute_acc(gold, pred, "n_killed")
    n_injured_acc = compute_acc(gold, pred, "n_injured")

    print("Address accuracy: " + str(addr_acc))
    print("Date accuracy: " + str(date_acc))
    print("Num killed accuracy: " + str(n_killed_acc))
    print("Num injured accuracy: " + str(n_injured_acc))

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

