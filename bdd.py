

import psycopg2
from datetime import datetime

import uuid

# hostname = 'localhost'
# database = 'firstDatabase'
# username = 'postgres'
# pwd = 'root'
# port_id = 5432
hostname = 'containers-us-west-121.railway.app'
database = 'railway'
username = 'postgres'
pwd = 'syRzvlDBmsXujDN4aKrJ'
port_id = 7801




def write_in_bdd(id, value, result):
    conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)   
    
    curr = conn.cursor()
    time = datetime.now()
    curr.execute("INSERT INTO botfair (bot_id, time, value, result) VALUES (%s, %s, %s, %s);", (id, time, value, result))
    conn.commit()

    print('criado com sucesso') 
    conn.close()
    curr.close()

def show_table():
    conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)   
    
    curr = conn.cursor()
    
    curr.execute("SELECT * FROM botfair")
    bots = curr.fetchall()
    bot_list = []
    for bot in bots:
        bot_list.append({
            'bot_id': bot[1],
            'time': bot[2],
            'message': bot[3]
        })
    conn.close()
    curr.close()
    return bot_list


def show_bot_by_id(bot_id):
    conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)   
    
    curr = conn.cursor()
    
    curr.execute(f"SELECT * FROM botfair WHERE bot_id = '{bot_id}';")
    bots = curr.fetchall()
    bot_list = []
    for bot in bots:
        bot_list.append({
            'bot_id': bot[1],
            'time': bot[2],
            'message': bot[3]
        })
    conn.close()
    curr.close()
    return bot_list


def create_stoped_bot(bot_id):
    conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)   
    curr = conn.cursor()
    curr.execute(f"INSERT INTO stoped_bots (bot_id) VALUES ('{bot_id}');")
    conn.commit()
    curr.close()
    conn.close()
    
def stoped_bots_list():
    conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)   
    
    curr = conn.cursor()
    
    curr.execute("SELECT * FROM stoped_bots")
    bots = curr.fetchall()
    bot_list = []
    for bot in bots:
        bot_list.append(bot[1])
    conn.close()
    curr.close()
    return bot_list
