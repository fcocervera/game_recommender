import psycopg2

def create_dbs():

	conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
	c = conn.cursor()

		# 100 most populous cities with associated zip code
	try:
	    c.execute('''
	    	CREATE TABLE IF NOT EXISTS zip_codes(
	        ID SERIAL PRIMARY KEY,
	        city TEXT,
	        state TEXT,
	        zip_code INT );
	    ''')
	except psycopg2.Error as e:
	    pass

	# 12,000 most popular board games by rank
	try:
	    c.execute('''
	    	CREATE TABLE IF NOT EXISTS board_games(
	        ID SERIAL PRIMARY KEY,
	        title TEXT,
	        avg_rating REAL,
	        rank INT,
	        num_votes INT,
	        imgurl TEXT );
	    ''')
	except psycopg2.Error as e:
	    pass

	# 12,000 usernames of those living within 100 miles of zip_codes.
	try:
	    c.execute('''
	    	CREATE TABLE IF NOT EXISTS user_names(
	        ID SERIAL PRIMARY KEY,
	        user_name TEXT,
	        city TEXT,
	        state TEXT );
	    ''')
	except psycopg2.Error as e:
	    pass

	# user, title ratings
	try:
	    c.execute('''
	    	CREATE TABLE IF NOT EXISTS title_rating(
	        ID SERIAL PRIMARY KEY,
	        user_name TEXT,
	        title TEXT,
	        rating REAL,
	        user_city TEXT,
	        user_state TEXT,
	        lat NUMERIC(14,9),
	        lon NUMERIC(14,9) );
	    ''')
	except psycopg2.Error as e:
	    pass

	conn.commit()
	conn.close()


