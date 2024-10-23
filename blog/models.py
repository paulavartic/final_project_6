from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Title',
        help_text='Enter the title of the post',
    )
    body = models.TextField(
        verbose_name='Body',
        help_text='Enter the text',
    )
    preview = models.ImageField(
        upload_to='blog/photo',
        verbose_name='Photo',
        help_text='Add a photo',
        blank=True,
        null=True,
    )
    created_at = models.DateField(
        verbose_name='Publication date',
        blank=True,
        null=True,
        default=timezone.now
    )
    views_count = models.PositiveIntegerField(
        verbose_name='Views',
        default=0,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
