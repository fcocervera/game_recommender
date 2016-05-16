## Recommender Capstone Project

### Introduction
For my Data Science Immersive capstone project at Galvanize, I built a recommender system for an online board game website. 


<p align="center">
  <img src="/img/hero.png">
</p>
### General Overview
Companies are looking to increase sales. Instead of randomly selecting items to display to visitors, they prefer a targeted approach that increases the likelihood of displaying an item the visitor will buy. Enter recommender engines!

In the Venn diagram below, where 'R' is our inventory of board games and 'V' is the board games our visitors are interestd in buying, recommenders will increase RUV to maximize the likelihood of a purchase. 

<p align="center">
  <img src="/img/venn.png">
</p>

### Recommender Build Process
* Scraped 600K data points, representing roughly 12,000 board games rated by 31,000 users.
* EDA to better understand density of matrix and distribution of ratings.
* Considered appropriate error metric for final model.
* Determined solution to 'cold start problem.'
* Built model using Graphlabs implementation of matrix factorization.
* Grid search to tune hyperparameters on AWS.
* Calculate precision and recall.
* Built prototpe with Flask and Zurb Foundation 6.
* Lastly, for fun I wanted to see if there were geographic areas of popularity for particular games. Meaning that if I recommended a board game, you could see a map demostrating where else this game was popular.

### Results
I opted to create a classification scoring model that predicted a users rating above or below a given threshold of 8. Instances correctly predicting above a 8, were True Positives (TP) and so forth. This allowed me the flexibility to tune the parameters with the aid of a confusion matrix and optimizing for precision and recall, with final results of ...

* Low Precision means high FP. We recommended something they didn't like. They're annoyed.
* Low Recall means high FN. We we didn't recommend something that they would have liked. They're missing out.

In a real world scenario, I would have optimized for precision/recall by A/B testing different settings and maximizing for conversions.

### Output
<p align="center">
  <img src="/img/output.png">
</p>

### Tools Used
* Python 2.7
* Graphlab
* PostreSQL
* psycopg2
* BeautifulSoup
* Flask
* Zurb Foundation 6
* AWS for Gridsearch

### File Descriptions
* `postgres.py` - Used to initialize database tables and schemas.
* `application.py` - Front-end of application built with Flask.
* `model_tuning.py` - Basic gridsearch over hyper-params
* `scraping.py` - Scrapers used to collect data.
* `models.py` - Collects main data and side data to build Graphlab model.
