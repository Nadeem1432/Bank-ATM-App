import pika
import json
from .models import ATMAccount

def callback(ch, method, properties, body):
    message = json.loads(body)
    account_number = message['account_number']
    pin = message['pin']
    balance = message['balance']

    try:
        ATMAccount.objects.create(account_number=account_number, pin=pin, balance=balance)
        print(f"Created ATM account for {account_number} with initial balance {balance}.")
    except Exception as e:
        print(f"Failed to create ATM account: {str(e)}")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='account_creation')
    channel.basic_consume(queue='account_creation', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()