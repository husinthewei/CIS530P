### How to run
1. Check requirements.txt for requirements and how to install
2. With 530_test_data.json in the same directory as script, type `python simple-baseline.py > pred.json`
3. Run scoring script on output and gold `python score.py --goldfile data/y_test --predfile pred.json`

### Description of baseline
The baseline model predicts four things:
- n_killed: The number of people killed is predicted by selecting the first number from the text or 0 if no numbers exist.
- n_injured: The number of people injured is predicted by selecting the first number from the text or 0 if no numbers exist.
- shooting_date: The shooting date is predicted as the day before the article publication or yesterday if no publication date.
- address: The shooting address is predicted by performing spaCy named entity recognition on the text, and selecting a the first word of type "FAC" or "LOC".

### Sample Output
`{'incident_id': 486327, 'n_killed': 8, 'n_injured': 8, 'shooting_date': '2013-05-15', 'address': ''}`
`{'incident_id': 481220, 'n_killed': 1800, 'n_injured': 1800, 'shooting_date': '2013-03-04', 'address': 'Wellington Village Apartments'}`

Note in incident_id 486327, address is empty. Many texts actually do not have words that are of type "FAC" or "LOC".

### Score
The following is the resulting score of running our scoring script on the baseline output:

Score:
`Address accuracy: 0.10589651022864019
Date accuracy: 0.1865222623345367
Num killed accuracy: 0.3008423586040915
Num injured accuracy: 0.2503008423586041`