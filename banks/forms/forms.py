from django import forms
from ..models import Bank

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'inst_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'swift_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'name': {'required': 'This field is required'},
            'description': {'required': 'This field is required'},
            'inst_num': {'required': 'This field is required'},
            'swift_code': {'required': 'This field is required'},
        }
