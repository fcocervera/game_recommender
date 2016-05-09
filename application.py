from models import fetch_mainmodel, build_mainmodel
from flask import Flask, render_template, request, redirect
import psycopg2
from collections import defaultdict

app = Flask(__name__)

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
    for title in recs['item_id']:
        c.execute("""   SELECT imgurl, avg_rating 
                        FROM board_games 
                        WHERE title = %s; """, (title, ))
        url = c.fetchall()
        imgUrls[title].append(url[0][0])
        imgUrls[title].append(url[0][1])
    conn.close()
    print recs

    return render_template('response.html', 
    						rec_one=recs['item_id'][0],
    						rec_two=recs['item_id'][1],
    						rec_three=recs['item_id'][2],
    						rec_four=recs['item_id'][3],
    						rec_five=recs['item_id'][4],

                            pic_one=imgUrls[recs['item_id'][0]][0],
                            pic_two=imgUrls[recs['item_id'][1]][0],
                            pic_three=imgUrls[recs['item_id'][2]][0],
                            pic_four=imgUrls[recs['item_id'][3]][0],
                            pic_five=imgUrls[recs['item_id'][4]][0], 

                            rating_one=imgUrls[recs['item_id'][0]][1],
                            rating_two=imgUrls[recs['item_id'][1]][1],
                            rating_three=imgUrls[recs['item_id'][2]][1],
                            rating_four=imgUrls[recs['item_id'][3]][1],
                            rating_five=imgUrls[recs['item_id'][4]][1]

                            )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)







