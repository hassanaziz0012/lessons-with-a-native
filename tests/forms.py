from django import forms
from .models import Test


# Create your forms here
class CreateTestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['test_name', 'test_directions']
        
class UpdateTestForm(forms.ModelForm):

    test_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Test
        fields = ['test_name', 'test_directions']
