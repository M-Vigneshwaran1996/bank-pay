# Bank-pay

In this project I created a structured streaming the transactions.<br>

- Producer:<br>
Simple Flask App by transactions through API.<br>
Flask App get that data and load to Kafka topic for every transaction.<br>

- Consumer:<br>
Kafka Consumer subscribe the kafka Producer and waiting for message data<br>
Consumer fetch the data and transforming using ingest_pipeline processors and writes to Elasticsearch.<br>

- Visualization:<br>
Kibana to visualize Elasticsearch data<br>

Data Flow

![image](https://github.com/user-attachments/assets/5ba58e3e-fabd-4f6f-8fae-31e91c1fc92f) 

Flask API
![image](https://github.com/user-attachments/assets/6c29d976-9dc9-4567-af10-e66f9e6e092b)

![image](https://github.com/user-attachments/assets/ede9584b-ac45-4fa1-8d33-da8ffd41d44f)


Elasticsearch
![image](https://github.com/user-attachments/assets/bb8c292c-8059-4dbb-a4c4-7cff98379387)


# Usage
<b>$ sudo docker-compose up -d --build</b> 
Flask App: <b> python flask-app/app.py</br>
Consumer : <b> python kafka-consumer/consumer.py</br>
Kibana Dashboard: <b> localhost:5602 </br>
