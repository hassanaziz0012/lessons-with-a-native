from django import forms
from .models import Question, StudentProfile, Test


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

class CreateTestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['test_name', 'test_directions']

class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question', 'answer']

class UpdateTestForm(forms.ModelForm):

    test_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Test
        fields = ['test_name', 'test_directions']

class UpdateQuestionForm(forms.ModelForm):

    question = forms.CharField(max_length=200, required=False)
    answer = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Question
        fields = ['question', 'answer']

class EmailStudentForm(forms.Form):

    recipient = forms.EmailField(label='Recipient\'s Email Address')
    subject = forms.CharField(max_length=120)
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['recipient', 'subject', 'body']




