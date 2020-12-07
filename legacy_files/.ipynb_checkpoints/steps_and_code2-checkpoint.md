Batch Steps
1 - Spin up environment using week 13 docker compose file
docker-compose up -d

2 - Create topic using kafka
docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

3 - Start flask api
docker-compose exec mids env FLASK_APP=/<file path>/game_api.py flask run --host 0.0.0.0

4 - Open terminal 2

5 - Generate events in terminal 2

while true; do
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/join_a_guild/1
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/kill_enemy/2
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/take_damage/3
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/accepted_a_quest/1
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/transaction/1001
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/join_a_guild/1
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/kill_enemy/2
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/take_damage/3
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/accepted_a_quest/3
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/transaction/1001
    sleep 10
done

5.5 - open terminal 3 

6 - Read events from Kafka in terminal 3
a. batch version
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning -e

6.5 - open terminal 4
    
7 - Run spark script file from terminal 4, i.e. running a job
new batch with write to database
docker-compose exec spark spark-submit /<file path>/write_data_batch.py

8 - Query using Presto
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
a. show tables
presto:default> show tables;
b. describe table
presto:default> describe <table_name>;
c. query table
presto:default> select * from <table_name>;

9 - Query purchase table and other tables for business analysis

----

Streaming Steps
1 - Spin up environment using week 13 docker compose file
docker-compose up -d

2 - Create topic using kafka
docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

3 - Start flask api
docker-compose exec mids env FLASK_APP=/<file path>/game_api.py flask run --host 0.0.0.0

4 - Open terminal 2

5 - Generate events in terminal 2

while true; do
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/join_a_guild/1
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/kill_enemy/2
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/take_damage/3
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/accepted_a_quest/1
        docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/transaction/1001
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/join_a_guild/1
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/kill_enemy/2
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/take_damage/3
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/accepted_a_quest/3
        docker-compose exec mids ab -n 10 -H "Host: user2.att.com" http://localhost:5000/transaction/1001
    sleep 10
done

5.5 - open terminal 3 

6 - Read events from Kafka in terminal 3
b. streaming version - removes -e to run continuously
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning

6.5 - open terminal 4

7 - Run spark script file from terminal 4, i.e. running a job
new stream
docker-compose exec spark spark-submit /<file path>/write_data_stream.py

7.5 - open terminal 5
    
8 - Create table in HDFS using Hive
for streaming follow these steps once to create tables
8.1 - navigate to same directory and run
docker-compose exec cloudera hive
8.2 - create tables
8.2.1 - this is failing
create external table if not exists default.transactions (Accept string, Host string, User_Agent string, event_type string, attributes string, store_id string, item_name string, inventory_id string, total_cost string, category string, on_hand_qty string, timestamp string) stored as parquet location '/tmp/transactions'  tblproperties ("parquet.compress"="SNAPPY");
8.2.2

8.2.3

8.2.4

8.2.5


9 - Query using Presto
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
a. show tables
presto:default> show tables;
b. describe table
presto:default> describe <table_name>;
c. query table
presto:default> select * from <table_name>;

10 - Query purchase table and other tables for business analysis