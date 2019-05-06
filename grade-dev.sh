python3 code/extensions.py --dev > output/pred_dev.json;
python3 score.py --predfile output/pred_dev.json --goldfile data/data-dev/y_val.json;