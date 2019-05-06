# Automated Information Extraction on Gun Violence News Articles
Our task is to extract pieces of information from gun violence news articles in the United States. The fields we are extracting are number of victims killed, number of victims injured, the incident date, and the address of the incident. 

## Requirements
spacy: 		pip install spacy
<br />
spacy en: 	python -m spacy download en
<br />
datetime:   pip install datetime

## Code Structure (in /code/)
* baseline contains the simple baseline as described in the writeup
* default contains the published baseline as described in the writeup
* extension-1 through extension-3 contain extensions to date, n_killed/n_injured, and address models respectively
* extensions.py runs all 3 extensions to produce predictions