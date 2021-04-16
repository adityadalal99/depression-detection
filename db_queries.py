import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(host = os.getenv('DB_host'), database = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PASSWORD'),port = os.getenv('DB_PORT'))

'''def db_connect():
    if conn == None:
        #conn = psycopg2.connect(host = os.getenv('DB_host'), database = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PASSWORD'))
    return conn'''


def get_default_ngo():
    #TODO : Get A default NGO query
    cur = conn.cursor()
    get_default_ngo_query = "SELECT ngo_id FROM ngo_details "
    return '41d5afd8-9c4f-11eb-a8b3-0242ac130003'


def get_ngo(coordinate_array):
    #conn = db_connect()
    cur = conn.cursor()
    get_ngo_query = "SELECT ngo_id FROM ngo_details WHERE ST_CONTAINS(ngo_location, ST_SetSRID(ST_MakePolygon( ST_GeomFromText('LINESTRING(%s %s,%s %s,%s %s,%s %s,%s %s)')),%s));"
    '''loc_string = ""
    for coordinate in coordinate_array:
        loc_string = loc_string + str(coordinate[0]) + " " + str(coordinate[1]) + ","
    loc_string = loc_string + str(coordinate_array[0][0]) + " " + str(coordinate_array[0][1])'''
    #print("SELECT ngo_id FROM ngo_details WHERE ST_CONTAINS(ngo_location, ST_SetSRID(ST_MakePolygon( ST_GeomFromText('LINESTRING(%s)')),4326))" % loc_string)
    try:
        cur.execute(get_ngo_query, (coordinate_array[0][0][0],coordinate_array[0][0][1],coordinate_array[0][1][0],coordinate_array[0][1][1],coordinate_array[0][2][0],coordinate_array[0][2][1],coordinate_array[0][3][0],coordinate_array[0][3][1],coordinate_array[0][0][0],coordinate_array[0][0][1], 4326,))
        ngo_id = cur.fetchone()
        print(ngo_id)
        if ngo_id is None:
            ngo_id = get_default_ngo()
        else:
            ngo_id = ngo_id[0]
        return ngo_id
    except Exception as e:
        coordinates = " ".join(str(x) for x in coordinate_array)
        print('Cannot get ngo_id for location' + coordinates + 'Error -- ' + str(e))


def check_user(user_id, coordinate_array):
    cur = conn.cursor()
    check_user_query = "SELECT user_id FROM depressed_users WHERE user_id = (%s)"
    try:
        cur.execute(check_user_query, (user_id,))
        user = cur.fetchone()
        print(user)
        if user is None:
            try:
                insert_user(user_id, coordinate_array)
            except Exception as e:
                print('User ' + str(user_id) + 'could not be added. Error -- ' + str(e))
    except Exception as e:
        print('Could Not find user' + str(user_id) + 'Error -- ' + str(e))


def insert_user(user_id, coordinate_array):
    cur = conn.cursor()
    insert_user_query = "INSERT INTO depressed_users (user_id,final_score,ngo_id) VALUES (%s, %s, %s)"
    ngo_id = get_ngo(coordinate_array)
    try:
        cur.execute(insert_user_query,(user_id, 1, ngo_id,))
        conn.commit()
    except Exception as e:
        print('Could Not Add User' + str(user_id) + 'Error -- ' + str(e))


def get_most_recent_tweet_of_user(user_id):
    cur = conn.cursor()
    get_most_recent_tweet_of_user_query = 'SELECT tweet_id_recent,tweets_count,tweets_score FROM depressed_users_tweets WHERE user_id = %s'
    try:
        cur.execute(get_most_recent_tweet_of_user_query,(user_id,))
        return cur.fetchone()
    except Exception as e:
        print('Could Not get most recent tweet id, count score of user ' + str(user_id) + ' Error --' + str(e))


def update_user_details(user_id,new_most_recent_id,curr_count,curr_score):
    cur = conn.cursor()
    update_user_details_query = 'UPDATE depressed_users_tweets SET tweet_id_recent = %s, tweets_count = %s, tweets_score = %s WHERE user_id = %s'
    try:
        cur.execute(update_user_details_query, (new_most_recent_id, curr_count, curr_score, user_id))
        conn.commit()
    except Exception as e:
        print('Could Not update most recent tweet id, count score of user' + user_id + 'Error --' + e)


def get_ngo_for_mail(user_id):
    cur = conn.cursor()
    get_ngo_for_mail_query = 'SELECT ngo_mail FROM ngo_details WHERE ngo_id = (SELECT ngo_id FROM depressed_users WHERE user_id = %s)'
    try:
        cur.execute(get_ngo_for_mail_query, (user_id,))
        return cur.fetchone()[0]
    except Exception as e:
        print('Could Not get ngo of user' + str(user_id) + 'Error --' + str(e))


def insert_tweet_with_details(user_id,tweet_id):
    cur = conn.cursor()
    insert_user_query = "INSERT INTO depressed_users_tweets (user_id,tweet_id_recent,tweets_count,tweets_score) VALUES (%s, %s, %s, %s)"
    try:
        cur.execute(insert_user_query, (user_id, tweet_id, 0, 0))
        conn.commit()
    except Exception as e:
        print('Could Not Add User With tweet details' + str(user_id) + 'Error -- ' + str(e))


def insert_ngo(coordinate_array, ngo_email, ngo_id, ngo_name):
    cur = conn.cursor()
    insert_user_query = "INSERT INTO ngo_details VALUES (%s, %s, %s, ST_SetSRID(ST_MakePolygon( ST_GeomFromText('LINESTRING(%s %s,%s %s,%s %s,%s %s,%s %s)')),%s));"
    try:
        cur.execute(insert_user_query, (ngo_id, ngo_email, ngo_name, coordinate_array[0][0],coordinate_array[0][1],coordinate_array[1][0],coordinate_array[1][1],coordinate_array[2][0],coordinate_array[2][1],coordinate_array[3][0],coordinate_array[3][1],coordinate_array[0][0],coordinate_array[0][1], 4326,))
        conn.commit()
    except Exception as e:
        print('Could Not Ngo with name ' + ngo_name + 'email' + ngo_email + 'Error -- ' + str(e))


def get_user_id_for_calc():
    cur = conn.cursor()
    get_user_id_for_calc_query = 'SELECT user_id FROM depressed_users_tweets WHERE TRUE'
    try:
        cur.execute(get_user_id_for_calc_query)
        return cur.fetchall()
    except Exception as e:
        print('Could Not get ngo of user' + str(user_id) + 'Error --' + str(e))

#SELECT ngoid WHERE st_contains(SELECT ST_MakePolygon( ST_GeomFromText('LINESTRING(75 29,77 29,77 29, 75 29)')))

'''pune_coordinates = [[73.8567, 18.5204], [73.8567, 18.5304], [73.8667, 18.5204], [73.8667, 18.5304]]
print(get_ngo(pune_coordinates))
print(get_most_recent_tweet_of_user(44196397)) 1380647716959645700'''
#print(get_most_recent_tweet_of_user(44196397)[2])

#22.7196° N, 75.8577° E
if __name__ == '__main__':
    insert_ngo([[75.8577, 22.7196], [77.1025, 28.7041], [87.8550, 22.9868], [78.4867, 17.3850], [75.8577, 22.7196]], 'dhairya189@gmail.com', '2f5a7434-9e29-11eb-a8b3-0242ac130003', 'Dhairyas')
'''24.5362, 81.3037
28.7041, 77.1025
22.9868, 87.8550
17.3850, 78.4867'''