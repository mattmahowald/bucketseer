import json
import time
import os
from google.cloud import pubsub_v1
import pika


def append_to_named_rabbitmq_queue(rabbitmq_queue_name):
    def _append_to_rmq_queue(raw_message):
        try:
            # TODO: cache pika connection and channel properly
            message = json.dumps({
                'data': json.loads(raw_message.data.decode('utf-8')),
                'msg_attributes': dict(raw_message.attributes)
            })
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', rabbitmq_credentials))
            channel = connection.channel()
            # TODO: add better exchange - routing_key semantics based on required workflow
            # see - https://www.youtube.com/watch?v=deG25y_r6OY
            channel.basic_publish(
                exchange='',
                routing_key=rabbitmq_queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)  # Make messages persistent
            )
            connection.close()
        except Exception as e:
            # TODO: Log when we fail to parse a message, shouldn't happen here
            print(f'Failed to parse message {raw_message} because of {e}')
            pass
        finally:
            raw_message.ack()
    return _append_to_rmq_queue


# Define callbacks for each subscription
# Each callback is a function that takes in one parameter (message) and does something
# ADD NEW SUBSCRIPTIONS HERE
callbacks = {
    'test-sub': append_to_named_rabbitmq_queue('test-sub-queue')
}


# Subscription configuration
project_id = os.environ['GCLOUD_PROJECT_ID']
subscription_names = list(callbacks.keys())

# RabbitMQ Authentication
rabbitmq_username = os.environ['RABBITMQ_USERNAME']
rabbitmq_password = os.environ['RABBITMQ_PASSWORD']
rabbitmq_credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)


def main():
    subscriber_clients = [pubsub_v1.SubscriberClient() for _ in range(len(subscription_names))]
    subscription_paths = [client.subscription_path(project_id, name) for client, name in zip(subscriber_clients, subscription_names)]
    for path, name, client in zip(subscription_paths, subscription_names, subscriber_clients):
        client.subscribe(path, callback=callbacks[name])

    # Loop and wait for messages to come in to hit callbacks
    while True:
        time.sleep(60)


if __name__ == '__main__':
    main()
