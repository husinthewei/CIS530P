### Evaluation ###
To evaluate models, we will be using accuracy scores for the four fields we are extracting:
- Date of shooting
- Address of shooting
- Number killed
- Number injured


Accuracy is simply calculated as (number correct) / (total)

Syntax is as follows: `python score.py --goldfile [goldfile] --predfile [predfile]`