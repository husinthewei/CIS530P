## Lit Review

1. This paper describes the motivation for the Gun Violence Database and how the authors began the automation of data collection using NLP tools. It first discusses how data on gun violence incidents is collected and annotated manually by humans and then how that data collection can be automated using NLP technology. In order to build up the original database, newspapers and articles are crawled and then classified by a machine learning high-recall text classifier. These classified documents are then passed on to human annotators that are able to verify the label. The human participants further annotated the articles by marking or highlighting important pieces of information relating to the incident, like the name of the shooter/victim(s), type of weapon used, location, etc. This results in an easily queryable, curated dataset. Next, the paper describes how the long and involved process of manual annotation can be streamlined using statistical NLP techniques. Modern NLP technologies exist for accurate Information Retrieval (getting the articles on incidents), NER and Event Detection (determine the key participants and details of the incident), Parsing and Coref (connecting articles relating to the same incident), and more. The authors argue that each piece of the original pipeline for populating the GVDB has been studied as its own NLP problem and that solutions readily exist to automate these processes. This is really important since the lack of good data (and funding for studies) has limited our ability to understand and tackle the issue of gun control. This paper shows that there is a promising method of extracting this important data with great accuracy, consistency and scalability using NLP.

2.  

3. 

# TODO: 1-2 paragraphs explaining which of the approaches you selected to re-implement as your baseline and why. 

 ### Works Cited

1. Pavlick, E. and Callison-Burch, C. (2016). The Gun Violence Database. Presented at the Data For Good Exchange 2016 (pp. 1-6).

2. Pavlick, E., Ji, H., Pan, X., & Callison-Burch, C. (2016). The Gun Violence Database: A new task and data set for NLP. In Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing (pp. 1018-1024).
