from django import forms
from customer.models import MenuItem

class EditForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'category', 'description', 'price')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }