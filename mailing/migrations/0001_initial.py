# Generated by Django 5.1.2 on 2024-10-12 22:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Enter email', max_length=254, verbose_name='Email')),
                ('full_name', models.CharField(help_text='Enter your full name', max_length=100, verbose_name='Full name')),
                ('comment', models.TextField(blank=True, help_text='Add a comment', max_length=200, null=True, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=300)),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_send', models.DateTimeField(default=django.utils.timezone.now)),
                ('frequency', models.CharField(choices=[('daily', 'Once a day'), ('weekly', 'Once a week'), ('monthly', 'Once a month')], max_length=15)),
                ('status', models.CharField(choices=[('created', 'Created'), ('running', 'Running'), ('completed', 'Completed')], default='created', max_length=25)),
                ('clients', models.ManyToManyField(to='mailing.client')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message')),
            ],
        ),
        migrations.CreateModel(
            name='SendingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('success', 'Successful'), ('failure', 'Failed')], max_length=15)),
                ('server_response', models.TextField(blank=True, null=True)),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailingsettings')),
            ],
        ),
    ]