python3 extensions.py --dev > pred_dev.json;
python3 score.py --predfile pred_dev.json --goldfile data-dev/y_val.json;