from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)

    completed = models.BooleanField(default=False)

    image = models.ImageField(
        upload_to='task_images/',
        null=True,
        blank=True
    )

    document = models.FileField(
        upload_to='task_docs/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title