baseline:
	python3 simple-baseline.py > pred.json

score:
	python3 score.py --predfile pred.json --goldfile data/y_test.json

clean:
	rm pred.json