from django import forms
from .models import *

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
