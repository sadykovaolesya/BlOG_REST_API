from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """Model Post"""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    read_users = models.ManyToManyField(User, related_name="read", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-time_create"]


class Subscribe(models.Model):
    """Model linking subscribers and authors"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_post"
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )

    class Meta:
        unique_together = ["author", "subscriber"]

    def __str__(self):
        return f"author = {self.author} subscriber = {self.subscriber}"
