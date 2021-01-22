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
        fields = ['test_name']

class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question', 'answer']

class UpdateTestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['test_name']





