from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User


class UploadFileForm(forms.Form):
    file  = forms.FileField()
    description = forms.CharField(max_length=50)


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))

    class Meta:
        model = Comment
        fields = ('author_name', 'text',)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=128)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def  clean_username(self):
        users = User.objects.filter(username=self.cleaned_data.get('username'))
        if len(users) > 0:
            raise forms.ValidationError("This username is already taken")

    def clean_email(self):
        emails = User.objects.filter(email=self.cleaned_data.get('email'))
        if len(emails) > 0:
            raise forms.ValidationError("This email is already taken")