# aside
ASIDE Project

- cat modelsega* >models.tar.gz
- tar -zxvf models.tar.gz

## Edit with current Public DNS (IPv4)

 sudo vi /etc/kafka/server.properties
  
## Start Confluent services  
 - sudo systemctl start confluent-zookeeper
 - sudo systemctl start confluent-kafka
 - sudo systemctl start confluent-schema-registry
 - sudo systemctl start confluent-kafka-rest
 - sudo systemctl start confluent-ksql
 
 - systemctl status confluent*
 - systemctl status confluent-*
  
## Check consumer  
 - kafka-avro-console-consumer --bootstrap-server localhost:9092 --topic videocap10 --property print.key=true --property print.value=false

## Check topic
 - kafka-topics --list --zookeeper localhost:2181



python TelloTV.py -sx 0 -sy 0 -os 1 -d 5

## Not working
python TelloTV.py -sx 0 -sy 0 -os 1 -d 5 -ss
python TelloTV.py -sx 0 -sy 0 -os 1 -d 1 -ss
python TelloTV.py -sx 350 -sy 350 -os 1 -d 3 -ss
python TelloTV.py -sx 0 -sy 350 -os 1 -d 3 -ss
python TelloTV.py -sx 50 -sy 50 -os 1 -d 3 -ss

## Works
python TelloTV.py -sx 50 -sy 50 -os 1 -d 0 -ss
python TelloTV.py -sx 350 -sy 350 -os 1 -d 0 -ss


