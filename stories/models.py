from django.db import models

from users.models import User


class Story(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    story = models.FileField(upload_to='media/stories/')

    def __str__(self):
        return self.title
