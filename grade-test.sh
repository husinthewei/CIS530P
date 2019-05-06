python3 code/extensions.py > output/pred_test.json;
python3 score.py --predfile output/pred_test.json --goldfile data/data-test/y_test.json;