from django.core.management.base import BaseCommand
from bank_app.consumers import start_consumer

class Command(BaseCommand):
    help = 'Run the RabbitMQ consumer for the Bank application'

    def handle(self, *args, **kwargs):
        start_consumer()