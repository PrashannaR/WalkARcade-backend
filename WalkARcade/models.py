from django.db import models

class UserPoints(models.Model):
    username = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)
    steps = models.IntegerField(default=0)

    def __str__(self):
        return self.username + " " + str(self.points)