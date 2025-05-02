# Bank-pay

In this project I created a structured streaming the transactions.<br>

- Producer:<br>
Simple Flask App by transactions through API.<br>
Flask App get that data and load to Kafka topic for every transaction.<br>

- Consumer:<br>
Kafka Consumer subscribe the kafka Producer and waiting for message data<br>
Consumer fetch the data and writes to Elasticsearch.<br>

- Visualization:<br>
Kibana to visualize Elasticsearch data<br>

Data Flow

[Client] → [Flask API] → [Kafka Producer] → [Kafka Topic]
                                      ↓
                               [Kafka Consumer]
                                      ↓
                              [Store to Elasticsearch]
                                      ↓
                                   [Kibana Visualization]

<b>$ sudo docker-compose up -d --build</b> 

# Usage
Flask App: python flask-app/app.py<br>
Consumer : python kafka-consumer/consumer.py<br>
Kibana Dashboard: localhost:5602 <br>
