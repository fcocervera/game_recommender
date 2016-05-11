## Recommender Capstone Project

<p align="center">
  <img src="/img/hero.png">
</p>

### General Overview


### Problem
Companies are looking to increase sales. Instead of randomly selecting items to display to visitors, they prefer a targeted approach that increases the likelihood of displaying an item the visitor will buy.

### Solution
In the Venn diagram below, where 'R' is our inventory of board games and 'V' is the board games our visitors are interestd in buying, recommenders will increase RUV to increase the likelihood of a purchase. 

![Alt text](/img/venn.png?raw=true "Image Title")

### Recommender Build Process
* Scraped 600K data points, representing roughly 12,000 board games rated by 31,000 users.
* EDA how many ratings per user, density of matrix
* Cold start problem.
* In the end I was able to achieve good results with x metrics.
* For fun I wanted to see if there were areas of popularity for certain games within different regions. So if I recommended a board game, you could see where else this game was popular.

### Results
Happy customers are now seeing more games they like and company making more revenue.

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
