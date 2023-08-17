from django import forms
from ..models import Bank, Branch

class BranchForm(forms.ModelForm):
    capacity = forms.IntegerField(required=False, min_value=0)
    
    class Meta:
        model = Branch
        fields = ['name', 'address', 'transit_num', 'email', 'capacity']

        error_messages = {
            'name': {'required': 'This field is required'},
            'address': {'required': 'This field is required'},
            'transit_num': {'required': 'This field is required'},
            'email': {'required': 'This field is required', 'invalid': 'Enter a valid email address'},
        }
        