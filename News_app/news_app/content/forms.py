from django import forms
from .models import Publisher
from accounts.models import EditorProfile, JournalistProfile, ReaderProfile
from accounts.models import Article, Newsletter


class ArticleForm(forms.ModelForm):
    '''Form for creating and editing articles.'''
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}), required=True)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'content'}), required=True)
    #author = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'author'}))
    publisher = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'publisher'}), required=False)

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        #self.fields['author'].queryset = JournalistProfile.objects.all()
        self.fields['publisher'].queryset = Publisher.objects.all()


class NewsletterForm(forms.ModelForm):
    '''Form for creating and editing newsletters.'''
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}), required=True)
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'content'}), required=True)
    articles = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'multiselect', 'placeholder':'articles'}))
    #author = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'author'}), required=False)
    publisher = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'publisher'}), required=False)
    #editor = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'editor'}), required=False)

    class Meta:
        model = Newsletter
        fields = ['title', 'description', 'articles', 'publisher']

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        #self.fields['author'].queryset = JournalistProfile.objects.all()
        self.fields['articles'].queryset = Article.objects.filter(approved=True)
        self.fields['publisher'].queryset = Publisher.objects.all()

class PublisherForm(forms.ModelForm):
    '''Form for creating and editing publishers.'''
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'name'}), required=True)

    class Meta:
        model = Publisher
        fields = ['name']


class JournalistForm(forms.ModelForm):
    '''Form for creating and editing journalist profiles.'''
    publishers = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'multiselect', 'placeholder':'publishers'}))

    class Meta:
        model = JournalistProfile
        fields = ['publishers']

    def __init__(self, *args, **kwargs):
        super(JournalistForm, self).__init__(*args, **kwargs)
        self.fields['publishers'].queryset = Publisher.objects.all()


class EditorForm(forms.ModelForm):
    '''Form for creating and editing editor profiles.'''
    publishers = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'multiselect', 'placeholder':'publishers'}), required=False)

    class Meta:
        model = EditorProfile
        fields = ['publishers']

    def __init__(self, *args, **kwargs):
        super(EditorForm, self).__init__(*args, **kwargs)
        self.fields['publishers'].queryset = Publisher.objects.all()


class ReaderForm(forms.ModelForm):
    '''Form for creating and editing reader profiles.'''
    publishers = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'multiselect', 'placeholder':'publishers'}), required=False)
    journalists = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'multiselect', 'placeholder':'journalists'}), required=False)

    class Meta:
        model = ReaderProfile
        fields = ['publishers', 'journalists']

    def __init__(self, *args, **kwargs):
        super(ReaderForm, self).__init__(*args, **kwargs)
        self.fields['publishers'].queryset = Publisher.objects.all()
        self.fields['journalists'].queryset = JournalistProfile.objects.all()