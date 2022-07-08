"""
Django command to wait for postgres db to be available
"""

import time
from django.db import OperationalError

# Operational error already exists so added the 'Op' in Psycopg2Error
# to differentiate the name
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        # stdout standard out prints it out to console
        self.stdout.write('Waiting for database..')
        db_up = False
        while db_up is False:
            try:
                # think self in this case is BaseCommand (from Django) check is
                # a function in BaseCommand
                # so self(basecommand).check --> checks the dbs in this case
                # default but its an array so you could check multiple dbs
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second..')
                time.sleep(1)
        # self style success just makes it green
        self.stdout.write(self.style.SUCCESS('Database available!'))
