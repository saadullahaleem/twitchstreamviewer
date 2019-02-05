import time
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        '''
            Some manage.py commands interact with the database, and we want
            them to be directly callable from `docker-compose run`. However,
            because docker may start the database container at the same time
            as it runs `manage.py`, we potentially face a race condition, and
            the manage.py command may attempt to connect to a database that
            isn't yet ready for connections.
            To alleviate this, we'll just wait for the database before calling
            the manage.py command.
            '''

        connection = connections[DEFAULT_DB_ALIAS]
        attempts = 0

        while True:
            try:
                connection.ensure_connection()
                break
            except OperationalError as e:
                if attempts >= 5:
                    raise e
                attempts += 1
                time.sleep(10)
                print("Attempting to connect to database.")

        print("Connection to database established.")