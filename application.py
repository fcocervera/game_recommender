from models import fetch_mainmodel, build_mainmodel
from flask import Flask, render_template, request, redirect
import psycopg2
from collections import defaultdict

app = Flask(__name__)

# Build and fetch main model for application
build_mainmodel()
model = fetch_mainmodel()

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    chosen_user = request.form['name']
    recs = model.recommend([chosen_user], k=5)

    imgUrls = defaultdict(list)
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
    c = conn.cursor()
    for title in recs['title']:
        c.execute("""   SELECT imgurl, avg_rating 
                        FROM board_games 
                        WHERE title = %s; """, (title, ))
        url = c.fetchall()
        imgUrls[title].append(url[0][0])
        imgUrls[title].append(url[0][1])
    conn.close()
    print recs

    return render_template('response.html', 
    			rec_one=recs['title'][0],
    			rec_two=recs['title'][1],
    			rec_three=recs['title'][2],
    			rec_four=recs['title'][3],
    			rec_five=recs['title'][4],

                        pic_one=imgUrls[recs['title'][0]][0],
	                pic_two=imgUrls[recs['title'][1]][0],
	                pic_three=imgUrls[recs['title'][2]][0],
	                pic_four=imgUrls[recs['title'][3]][0],
	                pic_five=imgUrls[recs['title'][4]][0], 
	
	                rating_one=imgUrls[recs['title'][0]][1],
	                rating_two=imgUrls[recs['title'][1]][1],
	                rating_three=imgUrls[recs['title'][2]][1],
	                rating_four=imgUrls[recs['title'][3]][1],
	                rating_five=imgUrls[recs['title'][4]][1]
	
	                )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)







