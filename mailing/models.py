from django.utils import timezone

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(
        verbose_name='Email',
        help_text='Enter email',
    )
    full_name = models.CharField(
        verbose_name='Full name',
        help_text='Enter your full name',
        max_length=100,
    )
    comment = models.TextField(
        verbose_name='Comment',
        help_text='Add a comment',
        max_length=200,
        **NULLABLE,
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.full_name} - {self.email}'


class Message(models.Model):
    subject = models.CharField(
        max_length=300
    )
    body = models.TextField()

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject


class MailingSettings(models.Model):
    FIRST_SEND_OPTIONS = (
        ('now', 'Instantly'),
        ('scheduled', 'Schedule'),
    )
    FREQUENCY_OPTIONS = (
        ('daily', 'Once a day'),
        ('weekly', 'Once a week'),
        ('monthly', 'Once a month'),
    )
    STATUS_OPTIONS = (
        ('created', 'Created'),
        ('running', 'Running'),
        ('completed', 'Completed'),
    )

    first_send = models.DateTimeField(
        default=timezone.now
    )
    frequency = models.CharField(
        max_length=15,
        choices=FREQUENCY_OPTIONS
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_OPTIONS,
        default='created'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )
    clients = models.ManyToManyField(Client)

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

    def __str__(self):
        return f'Mailing #{self.id}'


class SendingAttempt(models.Model):
    STATUS_OPTIONS = (
        ('success', 'Successful'),
        ('failure', 'Failed')
    )

    mailing = models.ForeignKey(
        MailingSettings,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_OPTIONS
    )
    server_response = models.TextField(
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Attempt'
        verbose_name_plural = 'Attempts'

    def __str__(self):
        return f"Mailing Attempt #{self.mailing_id}"
