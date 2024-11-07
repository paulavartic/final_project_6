from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import MailingSettings, Message


def get_mailing_from_cache():
    if not CACHE_ENABLED:
        return MailingSettings.objects.all()
    key = 'mailing_list'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = MailingSettings.objects.all()
    cache.set(key, mailings)
    return mailings


def get_messages_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = 'message_list'
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages
