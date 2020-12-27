from django import forms
from .models import Rate

class RateForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = Rate
        fields = ['rating',]