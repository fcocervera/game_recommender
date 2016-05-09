from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
import requests
import psycopg2
import time
import numpy as np

def scrape_zip_codes ():
	city = []
	state = []
	zip_codes = []

	# Prepare information for Requests
	url = 'http://localistica.com/usa/zipcodes/most-populated-zipcodes/'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
	(KHTML, like Gecko) Chrome/48.0.1564.116 Safari/537.36'}
    z = requests.get(url, headers=headers)
	bsObj = BeautifulSoup(z.content, "html.parser", from_encoding='UTF-8')

	# Grab city and state
	for x in bsObj.findAll('td', align='Left'):
	    city.append(' '.join(x.a.text.encode('utf8').split()[:-1]))
	    state.append(x.a.text.encode('utf8').split()[-1:][0])

	# Grab the zip code
	for i, x in enumerate(bsObj.findAll('td', align='Center')):
	    if i % 5 == 0:
	        zip_codes.append(x.a.text.encode('utf8'))

	# Establish connection
	conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
	c = conn.cursor()

	# Store data
	for city, state, zip_code in zip(city, state, zip_codes):
        c.execute("""INSERT INTO zip_codes (city, state, zip_code) 
                VALUES (%s, %s, %s);""", (city, state, zip_code))

	# Close connection
	conn.commit()
	conn.close()


def scrape_board_games():
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
	(KHTML, like Gecko) Chrome/48.0.1564.116 Safari/537.36'}

	for page_number in xrange(1, 119): # Stores the top 12,000 board games
	    url = 'https://boardgamegeek.com/browse/boardgame/page/%s' % page_number
    	z = requests.get(url, headers=headers)
	    bsObj = BeautifulSoup(z.content, "html.parser", from_encoding='UTF-8')

	    c = conn.cursor()

	    for i in xrange(100):
            try:
    	        title = bsObj.findAll('td', class_="collection_objectname")[i].a.text.encode('utf8')
    	        avg_rating = bsObj.findAll('td', class_="collection_bggrating")[i*3+1].text.encode('utf8').split('\t')[3]
    	        rank = bsObj.findAll('td', class_="collection_rank")[i].text.encode('utf8').split('\t')[3]
    	        num_votes = bsObj.findAll('td', class_="collection_bggrating")[i*3+2].text.encode('utf8').split('\t')[3]
                imgUrl = bsObj.findAll('td', class_='collection_thumbnail')[i].find(src=True)['src'].strip('//')

                c.execute("""INSERT INTO board_games (title, avg_rating, rank, num_votes, imgurl) 
                        VALUES (%s, %s, %s, %s, %s);""", (title[:100], avg_rating, rank, num_votes, imgUrl))
    	    	conn.commit()
            except TypeError:
                pass
		time.sleep(10) # Pause before next ping to server. Don't get blocked.
    conn.close()


def scrape_usernames(zip_codes):
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
    for zip_code in zip_codes:
        users = set()
        url = 'https://boardgamegeek.com/findgamers.php?action=findclosest&country=US&srczip=%s&maxdist=100&B1=Submit' % zip_code
	
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
		(KHTML, like Gecko) Chrome/48.0.1564.116 Safari/537.36'}	    
		z = requests.get(url, headers=headers)

        bsObj = BeautifulSoup(z.content, "html.parser", from_encoding='UTF-8')

        for x in bsObj.findAll('div', class_='username'):
            users.add(x.a.text.encode('utf8'))
            
        c = conn.cursor()
        for user in users:
            c.execute("""INSERT INTO user_names (user_name) VALUES (%s);""", (user,))
        conn.commit()
        time.sleep(10) # Pause before next ping to server. Don't get blocked.
        print 'Progress: %s done. Users %s' % (zip_code, len(users))

 	# Delete duplicates in case of overlap for zip code 100 mile radius.
    c = conn.cursor()
    c.execute(""" DELETE FROM user_names
						WHERE id IN (	SELECT id 
						FROM (SELECT id,
                      		ROW_NUMBER() OVER (partition BY user_name ORDER BY id) AS rnum
                 		FROM user_names) t
          				WHERE t.rnum > 1);""")
    conn.commit()
    conn.close()


def scrape_user_data(user):
    conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
	if len(user.split()) == 1:
		url = 'https://boardgamegeek.com/collection/user/%s' % (user)
	else:
		url = 'https://boardgamegeek.com/collection/user/%s' % ('%20'.join(user.split()))
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
	(KHTML, like Gecko) Chrome/48.0.1564.116 Safari/537.36'}
    z = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(z.content, "html.parser", from_encoding='UTF-8')

	title = []
	rating = []
	for x in bsObj.findAll('td', class_='collection_objectname'):
	    title.append(' '.join(x.text.encode('utf8').split()[:-1]))
	    
	for x in bsObj.findAll('div', class_='rating'):
	    rating.append(x.text.encode('utf8'))
	
	if title:
		c = conn.cursor()
		for title, rating in zip(title, rating):
		    if rating != 'N/A':
		    	rating = float(rating.strip('\n'))
        		c.execute("""INSERT INTO title_rating (user_name, title, rating) VALUES (%s, %s, %s);""", 
	            	(user, title[:100], rating))
        conn.commit()
    conn.close()
    time.sleep(15)
    # Used threadpool for this scrape.


def fetch_user_names():
	user_names = []

	conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
	c = conn.cursor()
	c.execute("""SELECT user_name FROM user_names;""")
	names = c.fetchall()
	conn.commit()
	conn.close()

	for name in names:
		user_names.append(name[0].strip())
	return user_names


def scrape_user_location(user):
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
        'WY': 'Wyoming'
    }
    states_long = set(states.values())
    states_abbrev = set(states.keys())
    states = states_abbrev.union(states_long)
    
    user_city = ''
    user_state = ''
    if len(user.split()) == 1:
        url = 'https://boardgamegeek.com/user/%s' % (user)
    else:
        url = 'https://boardgamegeek.com/user/%s' % ('%20'.join(user.split()))

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/48.0.1564.116 Safari/537.36'}

    z = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(z.content, "html.parser", from_encoding='UTF-8')
    try: # Very ugly, but this one had some interesting challenges.
        temp = str(bsObj.find('div', class_="location"))
        final = temp.replace('<div class="location js-location">', '').replace('</br>', '')\
            .replace('</div>', '').replace('United States', '').replace('<br>', '*').split('*')
        option1 = final[-1]
        option2 = final[-2]

        if option1 in states:
            user_state = option1
            user_city = option2
        else:
            user_state = option2
            user_city = option1  
    except IndexError:
        pass
        
    if user_city:
        conn = psycopg2.connect(dbname='capstone', user='franciscocervera', host='/tmp')
        c = conn.cursor()
        c.execute("""UPDATE user_names SET city=%s, state=%s WHERE user_name = %s;""", 
                    (user_city[:30], user_state[:30], user))
        conn.commit()
        conn.close()
    time.sleep(15)


if __name__ == '__main__':
	users_names = fetch_user_names()
	pool = ThreadPool(8) 
	pool.map(scrape_user_data, users_names)

	pool.close() 
	pool.join() 

