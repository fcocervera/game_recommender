import pandas as pd
import psycopg2
import numpy as np
import graphlab as gl


def fetch_mainmodel():
    return gl.load_model('game_recommender')


def build_mainmodel():
    data = build_maindata()
    print data
    sidedata = build_sidedata()
    model = gl.recommender.factorization_recommender.create( 
    						data, 
                            user_id="user_name", 
                            item_id="title", 
                            target="rating",
                            item_data=sidedata,
    						max_iterations=25,
    						num_factors=6,
    						regularization=0.001)
    model.save("game_recommender")


def build_sidedata():
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
    query = """     SELECT title_rating.title, avg_rating, num_votes 
                    FROM title_rating   
                    LEFT JOIN board_games         
                    ON title_rating.title = board_games.title        
                    WHERE avg_rating > 0;"""
    df = pd.read_sql_query(query, conn)
    conn.close()
    return gl.SFrame(data=df)

# COPY (SELECT user_name, title, rating FROM title_rating WHERE title IN (SELECT title FROM board_games)) To '/Users/franciscocervera/Desktop/output.csv' With CSV;

def build_maindata():
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
    query = """ SELECT user_name, title, rating 
                FROM title_rating 
                WHERE title_rating.title 
                IN (SELECT board_games.title FROM board_games);"""
    df = pd.read_sql_query(query, conn)
    conn.close()
    return gl.SFrame(data=df)


def map_games_region():
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')

    # Grab user info
    c = conn.cursor()
    c.execute("""SELECT user_name, city, state FROM user_names WHERE city IS NOT NULL;""")
    user_dump = c.fetchall()

    # Add to title_rating database and export to csv
    c = conn.cursor()
    for x in user_dump:
        if None not in x:       
            c.execute("""UPDATE title_rating SET user_city = %s, user_state = %s WHERE user_name = %s;""", 
                      (x[1], x[2], x[0]))
            conn.commit()    

    # Export relevant information to csv
    c = conn.cursor()
    df = pd.DataFrame(columns=['title', 'city', 'state'])
    c.execute("""SELECT title, user_city, user_state FROM title_rating WHERE user_city IS NOT NULL;""")
    map_dump = c.fetchall()
    conn.close()
    for x in map_dump:
        if None not in x:
            if x[2] in states:
                df = df.append({'title': x[0], 'city': x[1], 'state': states[x[2]]}, ignore_index=True)
            else:
                df = df.append({'title': x[0], 'city': x[1], 'state': x[2]}, ignore_index=True)
    df.to_csv('title_region_map.csv')
