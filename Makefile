baseline:
	python3 simple-baseline.py > pred.json

model:
	python3 baseline.py > pred.json

extension:
	python3 extension.py > pred.json

score:
	python3 score.py --predfile pred.json --goldfile data/y_test.json

clean:
	rm pred.json