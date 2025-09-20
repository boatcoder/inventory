from django import forms


class QueryForm(forms.Form):
    query_string = forms.CharField(widget=forms.Textarea())
    language = forms.CharField(required=False)
