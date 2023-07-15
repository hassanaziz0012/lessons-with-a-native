from django import forms


class ImportDataForm(forms.Form):
    csv_file = forms.FileField(required=True)

    class Meta:
        fields = ['csv_file']

