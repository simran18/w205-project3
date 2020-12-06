# Project 3: Understanding User Behavior

## Overview
As data scientists at a game development company, we are building a latest mobile game that has the following events:
(1) Buy Assets
(2) Join a Guild
(3) Kill Enemies
(4) Take damage

Each event has it's respective metadata characteric of such events. This report will walk through how an end-to-end data pipeline was created for this game. 

## Tasks Description 
### Building the API server to log kafka events


## Setting up the Data pipeline
In terminal 1:

* 1. Start shell script which will set up docker and run the API*

`sh start_api_server.sh`

In terminal 2:
(Make sure you're in the right directory.)
* 2. Randomly generate events using Python script *

`python3 api_call_script.py`
    
In terminal 3:
(Make sure you're in the right directory.)

* 3. Read generated events from Kafka, to run continuously in new stream*

`docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning`

In terminal 4: 
(Make sure you're in the right directory.)

* 4. Run spark script file from, i.e. running a job*

`docker-compose exec spark spark-submit /<file path>/write_data_stream_v3.py`

### Land them into HDFS/parquet to make them available for analysis using Presto

In terminal 5:
(Make sure you're in the right directory.)

* 5. Open Hive*:

`docker-compose exec cloudera hive`

* 6. Create tables in Hive*:

**GUILD_JOINS**
`create external table if not exists default.guild_joins 
(raw_event string, 
timestamp string, 
Accept string, 
Host string, 
User_Agent string, 
event_type string, 
guild_id bigint, 
name string) stored as parquet location '/tmp/guild_joins'  tblproperties ("parquet.compress"="SNAPPY");`
    
**ENEMY_KILLS**
`create external table if not exists default.enemy_kills (
raw_event string, 
timestamp string, 
Accept string, 
Host string, 
User_Agent string, 
event_type string, 
enemy_id bigint, 
name string, 
level smallint) stored as parquet location '/tmp/enemies_killed'  tblproperties ("parquet.compress"="SNAPPY");`

**QUESTS**
`create external table if not exists default.quests (
raw_event string, 
timestamp string, 
Accept string, 
Host string, 
User_Agent string, 
event_type string, 
quest_id bigint,
name string, 
contact string) stored as parquet location '/tmp/quest_accept'  tblproperties ("parquet.compress"="SNAPPY");`

**TAKE_DAMAGE**
`create external table if not exists default.take_damage (
raw_event string, 
timestamp string, 
Accept string, 
Host string, 
User_Agent string, 
event_type string, 
enemy_id bigint, 
name string, 
damage smallint) stored as parquet location '/tmp/damage_taken'  tblproperties ("parquet.compress"="SNAPPY");`
    
**TRANSACTIONS**
`create external table if not exists default.transactions (
raw_event string, 
timestamp string, 
Accept string, 
Host string, 
User_Agent string, 
event_type string, 
store_id bigint, 
item_name string, 
inventory_id bigint, 
total_cost float, 
category string, 
on_hand_qty smallint) 
stored as parquet location '/tmp/transactions'  
tblproperties ("parquet.compress"="SNAPPY");`

## Set up Presto for analysis
In terminal 6:
(Make sure you're in the right directory.)

* 7. Check if the tables exist in temp:*

`docker-compose exec cloudera hadoop fs -ls /tmp/`

* 8. Start presto:*

`docker-compose exec presto presto --server presto:8080 --catalog hive --schema default`

## Report Analysis (through Presto CLI)

* 9. First we'll look at the tables in HDFS*

`show tables;`

    Table     
--------------
 enemy_kills  
 guild_joins  
 quests       
 take_damage  
 transactions 



* 10. Next, let's understand the structure of each table.*

`describe enemy_kills;`

   Column   |  Type   | Comment 
------------+---------+---------
 raw_event  | varchar |         
 timestamp  | varchar |         
 accept     | varchar |         
 host       | varchar |         
 user_agent | varchar |         
 event_type | varchar |         
 enemy_id   | bigint  |         
 name       | varchar |         
 level      | integer |         


`describe quests;`

   Column   |  Type   | Comment 
------------+---------+---------
 raw_event  | varchar |         
 timestamp  | varchar |         
 accept     | varchar |         
 host       | varchar |         
 user_agent | varchar |         
 event_type | varchar |         
 quest_id   | bigint  |         
 name       | varchar |         
 contact    | varchar |         


`describe guild_joins;`
   Column   |  Type   | Comment 
------------+---------+---------
 raw_event  | varchar |         
 timestamp  | varchar |         
 accept     | varchar |         
 host       | varchar |         
 user_agent | varchar |         
 event_type | varchar |         
 guild_id   | bigint  |         
 name       | varchar |         


`describe transactions;`
    Column    |  Type   | Comment 
--------------+---------+---------
 raw_event    | varchar |         
 timestamp    | varchar |         
 accept       | varchar |         
 host         | varchar |         
 user_agent   | varchar |         
 event_type   | varchar |         
 store_id     | bigint  |         
 item_name    | varchar |         
 inventory_id | bigint  |         
 total_cost   | double  |         
 category     | varchar |         
 on_hand_qty  | integer |         


`describe take_damage;`
   Column   |  Type   | Comment 
------------+---------+---------
 raw_event  | varchar |         
 timestamp  | varchar |         
 accept     | varchar |         
 host       | varchar |         
 user_agent | varchar |         
 event_type | varchar |         
 enemy_id   | bigint  |         
 name       | varchar |         
 damage     | integer |         


* 11. Here's some business questions that can be answered with this data:*

* 1. How many different guilds exist currently?*

`select count(distinct name) as count_guild
from guild_joins;`

 count_guild 
-------------
          26 

* 2. How many guilds are called Templars?*

`select count(distinct name) as count_guild_templar
from guild_joins
where name like '%Templar';`

 count_guild_templar 
---------------------
                  10 


* 3. What is the most common quests?*

`select name, count(name) as total_quests
from quests
group by name
order by count(name) desc;`

                     name                      | total_quests 
-----------------------------------------------+--------------
 Are We There, Yeti?                           |            7 
 There Is No Rule 6                            |            7 
 Of Coursers We Know                           |            7 
 There is too much slaying and yapping         |            7 
 You Are Fired                                 |            7 


* 4. What are the least common contacts in quests?*

`select contact, count(contact) as total_counts
from quests
group by contact
order by count(contact) desc;`

       contact       | total_counts 
---------------------+--------------
 Bevel Right         |            4 
 Bevel Left          |            4 


* 5. What is average level of killing an enemy?*

`select round(avg(level),2) as average_level
from enemy_kills;`

 average_level 
---------------
         44.62 


* 6. Which user was killed on the lowest level?*

`select name, min(level) as low_level
from enemy_kills
group by name
order by min(level)
limit 2;`

      name       | low_level 
-----------------+-----------
 Private         |         1 
 Sheep           |         1 



* 7. Which game level has had the highest amount of kills?*

`select level, count(*) as total_kills
from enemy_kills
group by level
order by count(*) desc
limit 3;`

 level | total_kills 
-------+-------------
    56 |          10 
     7 |           7 
     4 |           6 


* 8. What is the costliest item?*

`select item_name, max(total_cost) as highest_cost
from transactions
group by item_name
order by max(total_cost) desc;`

  item_name   | highest_cost 
--------------+--------------
 Sacred Bow   |       1500.0 
 

* 9. What are the items that need to be replenished?*

`select item_name, min(on_hand_qty) as lowest_qty
from transactions
group by item_name
order by min(on_hand_qty);`

  item_name   | lowest_qty 
--------------+------------
 Sacred Bow   |          7 
 Master Sword |          7 
 Plate Armor  |          7 
 

* 10. What is highest total cost of each category?*

`select category, max(total_cost) as highest_cost
from transactions
group by category
order by max(total_cost) desc;`

 category | highest_cost 
----------+--------------
 Bow      |       1500.0 
 Sword    |       1000.0 
 Armor    |        500.0 
 

* 11. What is the total value of items, currently in each store?*

`select store_id, sum(total_cost * on_hand_qty) as total_value
from transactions
group by store_id;`

 store_id | total_value 
----------+-------------
        5 |    276500.0 
        1 |    175000.0 
        4 |    182000.0 
        2 |    248500.0 
        3 |    301000.0 
        

* 12. How many items are in each category?*

`select category, count(distinct item_name) as item_count_category
from transactions
group by category;`

 category | item_count_category 
----------+---------------------
 Bow      |          1 
 Armor    |          1 
 Sword    |          1 
 

* 13. How many items are in each store?*

`select store_id, count(distinct item_name) as item_count_store
from transactions
group by store_id;`

 store_id | item_count_store 
----------+------------------
        3 |                3 
        4 |                3 
        1 |                3 
        2 |                3 
        5 |                3 


* 14. Who has taken the highest amount of damage?*

`select name, max(damage) as highest_damage
from take_damage
group by name
order by max(damage) desc
limit 2;`

   name    | highest_damage 
-----------+----------------
 Dragon    |             99 
 John Wick |             67 
 

* 15. Which enemy has caused the highest damage?*

`select enemy_id, max(damage) as highest_damage
from take_damage
group by enemy_id
order by max(damage) desc
limit 3;`

 enemy_id | highest_damage 
----------+----------------
        1 |             99 
        5 |             67 
        8 |             57 
        