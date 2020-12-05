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

*1. Start shell script which will set up docker and run the API*
`sh start_api_server.sh`

In terminal 2:
(Make sure you're in the right directory.)
*2. Randomly generate events using Python script *
`python3 api_call_script.py`
    
In terminal 3:
(Make sure you're in the right directory.)

*3. Read generated events from Kafka, to run continuously in new stream*
`docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning`

In terminal 4: 
(Make sure you're in the right directory.)

*4. Run spark script file from, i.e. running a job*
`docker-compose exec spark spark-submit /w205/w205-project3/write_data_stream_v2.py`

### Land them into HDFS/parquet to make them available for analysis using Presto

In terminal 5:
(Make sure you're in the right directory.)

*5.Open Hive*:
`docker-compose exec cloudera hive`

*6.Create tables in Hive*:

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
damage string) stored as parquet location '/tmp/damage_taken'  tblproperties ("parquet.compress"="SNAPPY");`
    
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

Check if the tables exist in temp:
`docker-compose exec cloudera hadoop fs -ls /tmp/`

Start presto:
`docker-compose exec presto presto --server presto:8080 --catalog hive --schema default`

## Report Analysis (through Presto CLI)

First we'll look at the tables in HDFS
`show tables;`

Next, let's understand the structure of each table.
`describe enemy_kills;`

`describe quests;`

`describe guild_joins;`

`describe transactions;`

`describe take_damage;`

Here's some business questions that can be answered with this data:

*1. How many different guilds exist currently?*
`select count(distinct name) as count_guild
from guild_joins;`

*2. How many guilds are called Templars?*
`select count_if(name like '%Templar', distinct name) as count_guild_templar
from guild_joins;`

*3. What is the most common quests?*
`select name, count(name) as total_quests
from quests
order by count(name) desc;`// does not work (0 rows)

*4. What are the least common contacts in quests?*
`select contact, count(contact) as total_counts
from quests
order by count(contact) desc;`// does not work (0 rows)

*5. What is average level of killing an enemy?*
`select avg(cast(level as bigint)) as average_level
from enemy_kills;`
--  Unexpected parameters (varchar) for function avg. Expected: avg(double) , avg(bigint) 

*6. Who is the user who was killed on the lowest level?*
`select user_agent, min(level) as low_level
from enemy_kills
group by user_agent
order by min(level)
limit 2;`

*7. Which game level has had the highest amount of kills?*
`select level, count(*) as total
from enemy_kills
group by level
order by count(*) desc
limit 3;`


*8. What is the costliest item?*
`select item_name, max(total_cost) as highest_cost
from transactions
group by item_name;`
-- getting nulls even after casting as double

*9. What are the items that need to be replenished?*
`select item_name, min(on_hand_qty) as lowest_qty
from transactions
group by item_name;`

*10. What is highest total cost of each category?*
`select category, max(total_cost) as highest_cost
from transactions
group by category;`

*11. What is the total value of items, currently in each store?*
`selecct store_id, (total_cost * on_hand_qty) as total_value
from transactions
group by store_id;`


*12. What are the top 5 users who spent the most money?*
`select user_agent, sum(total_cost) as total_cost
from transactions
group by user_agent
order by sum(total_cost) desc
limit 5;`

*13. What are the 3 most popular categories , by users?*
`select category, count(user_agent) as count_category
from transactions
group by category
order by count(user_agent) desc
limit 3;`

*14. Who has taken the highest amount of damage?*
`select name, max(damage) as highest_damage
from take_damage
group by name
order by max(damage) desc
limit 2;`