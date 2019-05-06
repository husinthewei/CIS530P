# Automated Information Extraction on Gun Violence News Articles
Our task is to extract pieces of information from gun violence news articles in the United States. The fields we are extracting are number of victims killed, number of victims injured, the incident date, and the address of the incident. 

## Requirements
spacy: 		pip install spacy
spacy en: 	python -m spacy download en
datetime:   pip install datetime

## Code Structure
├── code
│   ├── baseline
│   │   ├── simple-baseline.md
│   │   └── simple-baseline.py
│   ├── default
│   │   ├── addressModel.py
│   │   ├── baseline.md
│   │   ├── baseline.py
│   │   ├── datePatterns.py
│   │   └── killedModel.py
│   ├── extension-1
│   │   ├── dateExtension.py
│   │   └── datePatterns.py
│   ├── extension-2
│   │   └── killedModelExtension.py
│   ├── extension-3
│   │   └── addressModelExtension.py
│   ├── extensions.md
│   └── extensions.py

* baseline contains the simple baseline as described in the writeup
* default contains the published baseline as described in the writeup
* extension-1 through extension-3 contains each of the extensions.
* extensions.py runs all 3 extensions to produce predictions.