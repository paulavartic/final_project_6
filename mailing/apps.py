from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    # def ready(self):
    #     from mailing.views import send_mailing
    #     sleep(2)
    #     send_mailing()
