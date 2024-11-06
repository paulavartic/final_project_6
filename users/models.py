import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE

default_code = ''.join([str(random.randint(0, 9)) for _ in range(12)])


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Email',
        help_text='Fill in your email address',
        unique=True
    )
    avatar = models.ImageField(
        verbose_name='Avatar',
        help_text='Add your photo',
        upload_to='users/',
        **NULLABLE
    )
    is_active = models.BooleanField(
        verbose_name='Active?',
        help_text='Activate user',
        default=True,
    )
    is_verified = models.BooleanField(
        verbose_name='Verified?',
        help_text='Verify email',
        default=False,
    )
    verification_code = models.CharField(
        verbose_name='Verification code',
        help_text='Fill in the code from email',
        max_length=15,
        default=default_code,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [
            ('can_block_user', 'Can block users'),
            ('can_view_users', 'Can view users')
        ]
