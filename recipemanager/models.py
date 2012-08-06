from django.db import models
from django.forms import ModelForm

# Create your models here.
class Recipe(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=400)
    added = models.DateTimeField(auto_now_add=True)
    last_made = models.DateTimeField()
    made_count = models.IntegerField()
    comments = models.TextField()

    def __unicode__(self):
        return self.title

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('url', 'title', 'comments')
