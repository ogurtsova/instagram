from django import forms


class UploadFileForm(forms.Form):
    file  = forms.FileField()
    description = forms.CharField(max_length=50)