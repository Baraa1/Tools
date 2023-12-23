from django import forms
from .models import *

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['position',]

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            "l_date": forms.DateInput(attrs={"type":"date"}),
        }

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = '__all__'
        widgets = {
            "i_date": forms.DateInput(attrs={"type":"date"}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            "t_date": forms.DateInput(attrs={"type":"date"}),
        }
