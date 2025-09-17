from django import forms

class PlaceForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Назва')
    description = forms.CharField(widget=forms.Textarea, required=True, label='Опис')
    type = forms.CharField(max_length=50, required=True, label='Тип')
    location = forms.CharField(max_length=100, required=False, label='Локація (необовʼязково)')
    rating = forms.IntegerField(min_value=1, max_value=5, required=True, label='Рейтинг (1–5)')
