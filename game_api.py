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


@app.route("/join_a_guild")
def join_a_guild():
    join_guild_event = {'event_type': 'join_guild', 
                        'attributes': {
                            "guild_name": "Data Masters"
                        }
                       }
    log_to_kafka('events', join_guild_event)
    return "Joined Guild!\n"


@app.route("/slay_a_dragon")
def slay_a_dragon():
    slay_a_dragon_event = {'event_type': 'slay_a_dragon', 
                           'attributes': {
                               'type': 'Norwegian Ridgeback'
                           }
                          }
    log_to_kafka('events', slay_a_dragon_event)
    return "Slayed A Dragon!\n"


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


@app.route("/accepted_a_quest")
def accept_quest():
    accept_quest_event = {'event_type': 'accept_quest', 
                          'attributes': {
                              'quest_name': 'Into The Breach', 
                              'quest_giver': 'Ronald McDonald'
                          }
                         }
    log_to_kafka('events', accept_quest_event)
    return "Quest Accepted!\n"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



@app.route("/transaction/<inventory_id>")
def transaction(inventory_id):
    
    """
    This function responds to a request for /api/transaction/{transaction_id}
    with one matching transaction from store_transactions.db
    
    :param inventory_id:  ID of the line item being transacted
    :return:              transaction matching ID
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
