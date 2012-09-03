from django.db import models
from django.forms import ModelForm, Form, CharField
from django.forms.widgets import RadioSelect
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, Reset
#from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField
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
    #Used for hash of recipe title (e.g. from Pinboard)--used for dupe detection
    hash = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100)
    tags = TaggableManager()
    RATING_CHOICES = (
            (1, '1 - Not Good'),
            (2, '2 - OK'),
            (3, '3 - Good'),
            (4, '4 - Very Good'),
            (5, '5 - Excellent - Going in the weekly rotation!'),
            )
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return self.title

class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('url', 'title', 'comments', 'made_count', 'tags', 'rating')

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
                Field('made_count', readonly='readonly', css_class="input-mini"),
                Field('tags', css_class='input-xxlarge'),
                Field('rating', widget='RadioSelect'),
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
        self.fields['made_count'].label = "Times Made"

class RecipeAjaxForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title',)

    #title = make_ajax_field(Recipe, 'title', 'recipe', help_text=None)
    title = AutoCompleteSelectField('recipe_add')

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

class RecipeAjaxSearchForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title',)

    #title = make_ajax_field(Recipe, 'title', 'recipe_search', help_text=None)
    title = AutoCompleteSelectField('recipe_search')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RecipeAjaxForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '/recipes/all/search'
        self.helper.layout = Layout(
                Field('title', css_class='input-xxlarge'),
                FormActions(
                    Submit('submit', 'Search', css_class='btn btn-primary btn-large')
                    )
                )

        super(RecipeAjaxSearchForm, self).__init__(*args, **kwargs)

class RecipeSearchForm(Form):

    term = CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'RecipeSearch'
        self.helper.form_class = "form-search"
        self.helper.form_method = "post"
        self.helper.form_action = "/recipes/search/"
        self.helper.layout = Layout(
                Field('term', css_class='input-xxlarge'),
                FormActions(
                    Submit('submit', 'Search', css_class='btn')
                    )
                )

        super(RecipeSearchForm, self).__init__(*args, **kwargs)
