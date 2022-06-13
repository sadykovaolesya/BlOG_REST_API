from enum import unique

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    read_users = models.ManyToManyField(User, related_name="read", blank=True)

    def get_read_status(self, request):
        return request.user in self.read_users.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-time_create"]


class Subscribe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_post"
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )

    class Meta:
        unique_together = ["author", "subscriber"]
