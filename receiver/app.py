from asyncio import events
import datetime
import json
import swagger_ui_bundle
import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def sellItem(body):

    trace = str(uuid.uuid4())
    body['trace_id'] = trace

    logger.info("Received event sellItem request with a trace id of " + trace)

    client = KafkaClient(hosts='100.25.199.62:9092')
    topic = client.topics[str.encode(events)]
    producer = topic.get_sync_producer()
    
    msg = { "type": "sell_item", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return f"Item sold", 201


def sales(body):

    trace = str(uuid.uuid4())
    body['trace_id'] = trace

    logger.info("Received event numSales request with a trace id of " + trace)

    client = KafkaClient(hosts='100.25.199.62:9092')
    topic = client.topics[str.encode(events)]
    producer = topic.get_sync_producer()
    
    msg = { "type": "num_sales", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return f"{body['profits']:.2f} made", 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("amazonAPI.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)