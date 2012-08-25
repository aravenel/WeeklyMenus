from django.db import models
from django.forms import ModelForm
from recipemanager.models import Recipe
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, Reset


# Create your models here.
class RecipeFeed(models.Model):
    FEED_CHOICES = (
            ('pinboard', 'Pinboard'),
            )
    feed_type = models.CharField(max_length=200, choices=FEED_CHOICES)
    feed_username = models.CharField(blank=True, null=True, max_length=200)
    feed_apikey = models.CharField(blank=True, null=True, max_length=300)
    feed_tag_key = models.CharField(blank=True, null=True, max_length=100)
    owner = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()

    def __unicode__(self):
        return "%s feed for %s" % (self.get_feed_type_display(), self.owner)

class RecipeFeedForm(ModelForm):

    class Meta:
        model = RecipeFeed
        fields = ('feed_type', 'feed_username', 'feed_apikey', 'feed_tag_key')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id_RecipeFeedForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
                Field('feed_type'),
                Field('feed_username', css_class='input-xxlarge'),
                Field('feed_apikey', css_class='input-xxlarge'),
                Field('feed_tag_key', css_class='input-xxlarge'),
                FormActions(
                    Submit('submit', 'Add Recipe Feed', css_class='btn-primary'),
                    Reset('reset', 'Reset', css_class='btn'),
                    )
                )

        super(RecipeFeedForm, self).__init__(*args, **kwargs)

        #Set field names
        self.fields['feed_username'].label = 'Feed Username'
        self.fields['feed_apikey'].label = 'Feed API Key'
        self.fields['feed_tag_key'].label = 'Tag to filter for recipes'
