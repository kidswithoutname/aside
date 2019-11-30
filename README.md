# aside
ASIDE Project

## Install project
 - pipenv shell
 - pip install opencv-python
 - pip install install opencv-contrib-python
 - pip install tensorflow==1.13.1
 - pip install matplotlib
 - pip install Pillow
 - pip install confluent_kafka
 - pip install confluent-kafka[avro]
 
## To generate the model directory
 - cat modelsega* >models.tar.gz
 - tar -zxvf models.tar.

 
OR pip install -r requirements.txt


## Some errors ans dolutions
__No module named 'cv2'__
 - pip install opencv-python
 
__AttributeError: module 'cv2.cv2' has no attribute 'face'__
 - pip install opencv-contrib-python
  - Check version: 4.1.2.30
 
__No module named 'tensorflow'__
 - pip install tensorflow==1.13.1
 
__No module named 'matplotlib'__
 - pip install matplotlib
 
__No module named 'PIL'__
 - pip install Pillow
 
__No module named 'confluent_kafka'__
 - pip install confluent_kafka
 
__No module named 'avro'__
 - pip install confluent-kafka[avro]

__Module 'tensorflow' has no attribute 'placeholder'__
 - pip uninstall tensorflow
 - pip install tensorflow==1.13.1
 
 
## Enter into aws machine
 - ssh -i ~/.ssh/keys/acl-fullAdmin.pem centos@<public-ip>

 
## Edit with current Public DNS (IPv4)

 - sudo vi /etc/kafka/server.properties
 ```text
 advertised.listeners=PLAINTEXT://<public-dns>:9092
 ```

  
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

 

## Not working
 - python TelloTV.py -sx 0 -sy 0 -os 1 -d 5 -ss
 - python TelloTV.py -sx 0 -sy 0 -os 1 -d 1 -ss
 - python TelloTV.py -sx 350 -sy 350 -os 1 -d 3 -ss
 - python TelloTV.py -sx 0 -sy 350 -os 1 -d 3 -ss
 - python TelloTV.py -sx 50 -sy 50 -os 1 -d 3 -ss

## Works mmm
 - python TelloTV.py -sx 50 -sy 50 -os 1 -d 0 -ss
 - python Navigator.py -sx 350 -sy 350 -os 1 -d 0 -ss
 - python Navigator.py -sx 0 -sy 0 -os 1 -d 5 -ss
 
 ## Atras
 - python Navigator.py -sx 0 -sy 0 -os 1 -d 5 -ss
 
 ## Works kinda perfect
 python Navigator.py -sx 350 -sy 200 -os 1 -d 0 -os 3 -ss


