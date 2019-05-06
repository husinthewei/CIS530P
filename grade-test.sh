python3 extensions.py > pred_test.json;
python3 score.py --predfile pred_test.json --goldfile data-test/y_test.json;