#!/bin/bash

docker-compose up

docker-compose exec kafka \
   kafka-topics  \
     --create \
     --topic events \
     --partitions 1 \
     --replication-factor 1 \
     --if-not-exists --zookeeper zookeeper:32181

docker-compose exec mids \
    env FLASK_APP=/w205/project-3-cal-dortiz/game_api.py \
    flask run --host 0.0.0.0
