### How to run
1. Check requirements.txt for requirements and how to install
2. With 530_test_data.json in the same directory as script, type `python simple-baseline.py > pred.json`
3. Run scoring script on output and gold

### Description of baseline
The baseline model predicts four things:
- n_killed: The number of people killed is predicted by selecting a random number from the text or 0 if no numbers exist.
- n_injured: The number of people injured is predicted by selecting a random number from the text or 0 if no numbers exist.
- n_pred_shooting_date: The shooting date is predicted as the day before the article publication or yesterday if no publication date.
- address: The shooting address is predicted by performing spaCy named entity recognition on the text, and selecting a random word of type "FAC" or "LOC".

### Sample Output
`{'incident_id': 481208, 'n_killed': 10, 'n_injured': 23, 'shooting_date': '2013-03-02', 'address': ''}`
`{'incident_id': 486005, 'n_killed': 2, 'n_injured': 40, 'shooting_date': '2013-05-02', 'address': 'South 16th'}`

Note in incident_id 481208, address is empty. Many texts actually do not have words that are of type "FAC" or "LOC".

### Score
The following is the resulting score of running our scoring script on the baseline output:
Score: