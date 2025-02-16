import pika
import json
from .models import Account
from decimal import Decimal

def callback(ch, method, properties, body):
    message = json.loads(body)
    account_number = message['account_number']
    amount = Decimal(message['amount'])

    try:
        bank_account = Account.objects.get(account_number=account_number)
        bank_account.balance += amount
        bank_account.save()
        print(f"Updated bank account {account_number} with amount {amount}. New balance: {bank_account.balance}")
    except Account.DoesNotExist:
        print(f"Bank account {account_number} does not exist.")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='transaction')
    channel.basic_consume(queue='transaction', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()