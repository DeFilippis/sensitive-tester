from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate, class_prepared, pre_migrate
from django.db.backends.signals import connection_created


class TesterConfig(AppConfig):
    name = 'tester'

    def ready(self):
        """
        I've been considering of generating db records for proto Q here, but
        seems it's not the right place

        """
        print('TESTER READY')
