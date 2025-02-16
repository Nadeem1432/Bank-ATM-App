from django.core.management.base import BaseCommand
from atm_app.consumer import start_consumer

class Command(BaseCommand):
    help = 'Run the RabbitMQ consumer for the ATM application'

    def handle(self, *args, **kwargs):
        start_consumer()