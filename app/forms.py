from django import forms
from .models import Post, Comment


class UploadFileForm(forms.Form):
    file  = forms.FileField()
    description = forms.CharField(max_length=50)


class CommentForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))

    class Meta:
        model = Comment
        fields = ('author_name', 'text',)