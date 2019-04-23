import re
import datetime

# date pattern is (regex, strptime pattern)
date_patterns = [ 
    ("\w{4,} \d{1,2}, \d{4}", "%B %d, %Y"), # Janurary 21, 2017
    ("\w{3} \d{1,2}, \d{4}", "%B %d, %Y"), # Jan 21, 2017
    ("\d{1,2}/\d{1,2}/\d{2}", "%m/%d/%y"), # 10/21/08 or 1/1/03
    ("\d{1,2}/\d{1,2}/\d{4}", "%m/%d/%Y"), # 10/21/2008
    ("\d{4}-\d{1,2}-\d{1,2}", "%Y-%m-%d")  # 2008-01-15
]

day_pattern = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"

day_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

# Input: The text of the article
# Returns: A datetime object or None if there was no match
def match_date(text):
    for pattern in date_patterns:
        match = re.search(pattern[0], text)
        if match is not None:
            raw_date = match.group(0)
            event_date = datetime.datetime.strptime(raw_date, pattern[1])
            return event_date
        return None

# Input: The text of the article
# Input: The published date of the article
# Returns: A datetime object or None if there was no match
def match_day(text, published_date):
    reference_date = datetime.datetime.strptime(published_date, "%Y-%m-%d")
    match = re.search(day_pattern, text)
    if match is not None:
        day = match.group(0)
        day_idx = day_map[day]
        diff = day_idx - reference_date.weekday()
        if diff > 0:
            diff = diff - 7
        event_date = reference_date + datetime.timedelta(days=diff)
        return event_date
    return None

# Input: The text of the article
# Input: The published date of the article
# Returns: A datetime object or None if there was no match
# Can do more complicated analysis. The first date seen is not necessarily the date that someone died. Can modify the above dates to return a list of them.
def find_date(text, published_date):
    res = match_day(text, published_date)
    if res is not None:
        return res
    res = match_date(text)
    return res




    
