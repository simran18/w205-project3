#!/usr/bin/env python
import json
import sqlite3
from kafka import KafkaProducer
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#Done
@app.route("/join_a_guild/<guild_id>")
def join_a_guild(guild_id):
    
    """
    This function responds to a request for /api/join_a_guild/{guild_id}
    with one matching transaction from quest.db
    
    :param guild_id:      ID of the enemy
    :return:              quest and attributes matching ID as JSON
    """
    
    query = "SELECT * \
             FROM guild \
             WHERE guild_id =" + str(guild_id) +';'

    conn = sqlite3.connect('/w205/project-3-cal-dortiz/guild.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query).fetchall()
    
    print(results)
    
    join_guild_event = {'event_type': 'join_guild', 
                        'attributes': results[0]}
    
    log_to_kafka('events', join_guild_event)
    return "Joined Guild!\n"


@app.route("/kill_enemy/<enemy_id>")
def kill_enemy(enemy_id):
    
    """
    This function responds to a request for /api/kill_enemy/{enemy_id}
    with one matching transaction from quest.db
    
    :param enm,y_id:      ID of the enemy
    :return:              quest and attributes matching ID as JSON
    """
    
    query = "SELECT * \
             FROM enemy \
             WHERE enemy_id =" + str(enemy_id) +';'
    
    conn = sqlite3.connect('/w205/project-3-cal-dortiz/enemy.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query).fetchall()
    
    kill_enemy_event = {'event_type': 'kill_enemy', 
                           'attributes': results[0]}
    
    log_to_kafka('events', kill_enemy_event)
    return "kill_enemy!\n"


@app.route("/take_damage")
def take_damage():
    take_damage_event = {'event_type': 'take_damage',
                         'attributes': {
                             "damage_taken": "1", 
                             'enemy': 'Mr Meeseeks'
                         }
                        }
    log_to_kafka('events', take_damage_event)
    return "Took Damage!\n"


@app.route("/accepted_a_quest/<quest_id>")
def accept_quest(quest_id):
    
    """
    This function responds to a request for /api/accepted_a_quest/{quest_id}
    with one matching transaction from quest.db
    
    :param quest_id:      ID of the quest
    :return:              quest and attributes matching ID as JSON
    """
    
    query_1 = "SELECT * \
             FROM quest \
             WHERE quest_id =" + str(quest_id) +';'
    
    conn = sqlite3.connect('/w205/project-3-cal-dortiz/quest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query_1).fetchall()
        
    accept_quest_event = {'event_type': 'accept_quest', 
                          'attributes': results[0]}
    
    log_to_kafka('events', accept_quest_event)
    return "Quest Accepted!\n"


@app.route("/transaction/<inventory_id>")
def transaction(inventory_id):
    
    """
    This function responds to a request for /api/transaction/{transaction_id}
    with one matching transaction from store_transactions.db
    
    :param inventory_id:  ID of the line item being transacted
    :return:              transaction and attributes matching ID as JSON
    """
    
    query = "SELECT * \
             FROM inventory \
             WHERE inventory_id =" + str(inventory_id) +';'
    
    conn = sqlite3.connect('/w205/project-3-cal-dortiz/store_transactions.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query).fetchall()
    #print(results)
    #print(results[0])
    
    transaction_event = {'event_type': 'transaction', 
                         'attributes': results[0]}
    
    log_to_kafka('events', transaction_event)
    return "Transaction Complete!\n"  
