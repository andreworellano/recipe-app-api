"""
Test custom django management commands
"""
# this is the built in python unittest class with mock function that
# helps mimick certain functionality
from unittest.mock import patch

# type of error we might get if we try to connect to the DB before it's ready
# this error happens in postgres when the server is trying to connect
from psycopg2 import OperationalError as Psycopg2Error

# helper function to call the command we're testing
from django.core.management import call_command
# another error that can be thrown by the db
# this one is specific to django when the database itself
# isn't ready it's a different error than the postgres error
from django.db.utils import OperationalError
# base test class from django
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test command"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # \ is a way to break the line to keep it clean
        # the testing 2 then 3 times is arbitary just a rough estimate
        # of what would happen in reality
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
