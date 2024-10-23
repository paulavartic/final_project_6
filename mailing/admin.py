from django.contrib import admin

from mailing.models import Client, MailingSettings, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',)


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'frequency', 'message',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', )
    
