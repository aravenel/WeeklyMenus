from django.db import models

# Create your models here.
class Recipe(models.Model):
    url = models.URLField()
    added = models.DateTimeField(auto_now_add=True)
    last_made = models.DateTimeField()
    made_count = models.IntegerField()
    comments = models.TextField()
