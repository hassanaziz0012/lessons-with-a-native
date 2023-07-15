from django import forms
from .models import Question


class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question', 'answer']


class UpdateQuestionForm(forms.ModelForm):

    question = forms.CharField(max_length=200, required=False)
    answer = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Question
        fields = ['question', 'answer']