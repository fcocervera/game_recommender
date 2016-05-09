## Recommender Capstone Project

### File Descriptions
	- `postgres.py` - Used to initialize database tables and schemas.
	- `application.py` - Front-end of application built with Flask.
	- `model_tuning.py` - Basic gridsearch over hyper-params
	- `scraping.py` - Scrapers used to collect all relavent data for project.
	- `models.py` - Collects main data and side data to build Graphlab model.

### Problem
In general, the problem recommenders are trying to solve is showing website visitors items that they are likely to be interested in buying. In the Venn diagram below, 'R' is our inventory of board games and 'V' is the board games our visitors are interestd in buying. The union of the two, RUV, is the board games that site visitors are shown and are likely to want to purchase. Recommenders are looking to increase the size of RUV and thus increase the likelihood of a sale to increase revenue.  

![Alt text](/img/venn.png?raw=true "Image Title")

### Solution
I built a recommender that allows the system to leverage games that you’ve liked and match you with games that otter’s with similar interests also liked. It’s how Amazon recommends you books. 


### Process
-  I built a recommender that and chose to build one with high precision and low recall
- Scraped 600K data points, representing about 12,000 board games and 31,000 users.
- EDA how many ratings per user, density of matrix
- Cold start problem.
- In the end I was able to achieve good results with x metrics.
- For fun I wanted to see if there were areas of popularity for certain games within different regions. So if I recommended a board game, you could see where else this game was popular.
- I used x, y, z

### Closing
- Happy customers are now seeing more games they like and company making more revenue.

