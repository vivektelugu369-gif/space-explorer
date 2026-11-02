from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Favourites(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    image_url = models.URLField()
    explanation = models.TextField()

    class Meta:
        unique_together = ('user','date')

    def __str__(self):
        return self.title