from django import forms
from .models import StudentProfile, EmailPreset


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['username', 'email']

class UpdateStudentProfileForm(forms.ModelForm):

    username = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = StudentProfile
        fields = ['username', 'email']

class EmailStudentForm(forms.ModelForm):
    recipient = forms.EmailField(label='Recipient\'s Email Address')

    class Meta:
        model = EmailPreset
        fields = ['recipient', 'subject', 'body']
