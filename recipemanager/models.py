from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, Reset
from ajax_select import make_ajax_field
#from taggit.managers import TaggableManager
from taggit_autosuggest.managers import TaggableManager

# Create your models here.
class Recipe(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=400)
    added = models.DateTimeField(auto_now_add=True)
    last_made = models.DateTimeField(null=True,blank=True)
    made_count = models.IntegerField(null=True,blank=True,default=0)
    comments = models.TextField(null=True,blank=True)
    owner = models.ForeignKey(User)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('url', 'title', 'comments', 'tags')

    #crispy-forms setup stuff
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RecipeForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
                Field('url', css_class='input-xxlarge'),
                Field('title', css_class='input-xxlarge'),
                Field('comments', rows='5', css_class='input-xxlarge'),
                Field('tags', css_class='input-xxlarge'),
                FormActions(
                    Submit('submit', 'Add Recipe', css_class='btn-primary'),
                    Reset('reset', 'Reset', css_class='btn'),
                    )
                )

        #self.helper.add_input(Submit('submit', 'Submit'))

        super(RecipeForm, self).__init__(*args, **kwargs)

        #Set field labels
        self.fields['url'].label = "Recipe URL"
        self.fields['title'].label = "Recipe Title"

class RecipeAjaxForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title',)

    title = make_ajax_field(Recipe, 'title', 'recipe', help_text=None)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RecipeAjaxForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
                Field('title', css_class='input-xxlarge'),
                FormActions(
                    Submit('submit', 'Add Recipe to Menu', css_class='btn btn-primary btn-large')
                    )
                )

        super(RecipeAjaxForm, self).__init__(*args, **kwargs)
