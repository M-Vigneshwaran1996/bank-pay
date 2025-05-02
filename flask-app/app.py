# flask_app/app.py
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import time, random
from kafka import KafkaProducer
import json

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "c+pKBtFE8U9TnQ2j29ok"), verify_certs=False)

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda x: json.dumps(x).encode('utf-8'))


if not es.ping():
    raise ValueError("Connection failed")
else:
    print("*********Connected to Elasticsearch")


def send_transaction_to_kafka(transaction):
    try:
        print("Sending transaction to Kafka:", transaction)
        producer.send("payment_transactions", transaction)
        producer.flush()
    except Exception as e:
        print("Kafka send failed:", e)



@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.get_json()

    transaction_payload = {
        "account_holder": data.get("account_holder"),
        "account_number": data.get("account_number"),
        "transaction_id": random.randrange(1000,9999),
        "transaction_type": data.get("transaction_type"),
        "transaction_status": data.get("transaction_status"),
        "transaction_amount": data.get("transaction_amount"),
        "user_id": data.get("user_id"),
        "timestamp": time.time()
    }

    send_transaction_to_kafka(transaction_payload)

    return jsonify({"message": "Transaction sent to Kafka!"}), 200


@app.route('/get-transactions', methods=['GET'])
def get_transactions():
    status = request.args.get('status')
    print("Status*****************:", status)
    query = {
        "query": {
            "match": {'transaction_status': status}
        } if status else {
            "match_all": {}
        }
    }
    print("Query :", query)
    data = es.search(index='payment_transactions', body=query)
    transactions = [hit['_source'] for hit in data['hits']['hits']]
    return jsonify(transactions), 200



if __name__ == '__main__':
    app.run(debug=True)
