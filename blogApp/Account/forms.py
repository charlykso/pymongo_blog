from django import forms

class UpdateProfileForm(forms.Form):
    img = forms.FileField(required=False)
    profilePic = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=15, required=False)
    githubUsername = forms.CharField(max_length=100, required=False)
