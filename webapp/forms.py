from django import forms

class UploadCardSetForm(forms.Form):
    name = forms.CharField(max_length=80)
    file = forms.FileField()

class UploadUserLogsForm(forms.Form):
    file = forms.FileField()
