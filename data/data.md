## Introduction
The raw data come from the website https://www.kaggle.com/jameslko/gun-violence-data. Each event states the address, number killed, number injured, shooting date, the source article, and more. We used each event to get the training data. In particular, we extracted the contents of each article using a python library called newspaper, and compiled the event id, title, publish date, address, number killed, number injured, and the shooting date into a json object. 

Taking this filtered json file, we then bifurcated the data into the features and the labels where the features have title and publish date, and the labels have number address, killed, number injured, and shooting date.

## File structure
* In the data-* folders, we have all the splitted training, development, and testing files

## Dataset
We currently have 2338 samples. With the current splitting scheme, we are allocating 70% of the data to training, 9% to validation, and 21% to testing.

## Scripts
run `python separate_data.py` to split the data into train-dev-test files. 
run `python extract.py` with arguments to scrape articles from the dataset. Note that the dataset must be in the same directory. 
