from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "c+pKBtFE8U9TnQ2j29ok"), verify_certs=False)

if not es.ping():
    print("*********Connection failed")
    raise ValueError("Connection failed")
else:
    print("Connected to Elasticsearch")

ingest_pipeline = {
    "description": "Ingest pipeline for transaction data",
    "processors": [
        {
            "set": {
                "field": "bank",
                "value": "HDFC Bank"
            }
        },
        {
            "uppercase": {
                "field": "bank"
            }
        }
    ]
}

es.ingest.put_pipeline(id='transaction_pipeline', body=ingest_pipeline)

if not es.indices.exists(index='payment_transactions'):
    es.indices.create(index='payment_transactions', ignore=400)

consumer = KafkaConsumer(
    'payment_transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='transactions_group_1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("*********Kafka consumer started and subscribed to topics:", consumer.subscription())


for message in consumer:
    transaction = message.value
    print("Received transaction:**********", transaction)
    es.index(index='payment_transactions', body=transaction, pipeline='transaction_pipeline')
    print(f"Indexed transaction: {transaction}")