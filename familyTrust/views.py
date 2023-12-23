from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from .models import Transaction
from .forms import *

class Trust(LoginRequiredMixin, TemplateView):
    template_name = 'familyTrust/trust.html'
    transactions  = Transaction.objects.all()
    members       = Member.objects.all()
    members_list  = []#.aggregate(total=Sum('amount'))['total_subs']
    for member in members:
        member_dict  = {}
        member_dict['ar_name'] = f'{member.ar_name}'
        member_dict['transactions'] = len(Transaction.objects.filter(sender = member))
        member_dict['no_of_subs'] = len(Transaction.objects.filter(sender = member).exclude(subscription__isnull=True))
        member_dict['total_subs'] = Transaction.objects.filter(sender = member).exclude(subscription__isnull=True).aggregate(total_subs=Sum('amount'))['total_subs']
        member_dict['total_debt'] = Transaction.objects.filter(t_receiver = member).exclude(loan__isnull=True).aggregate(total_debt=Sum('amount'))['total_debt']
        members_list.append(member_dict)
    #print(transactions)
    total_income    = 0
    existing_total  = 0
    difference      = 0
    for transaction in transactions:
        total_income   += transaction.amount if transaction.positive else 0
        existing_total = (existing_total + transaction.amount) if transaction.positive else (existing_total - transaction.amount)
    extra_context = {
        'total_income': total_income,
        'existing_total': existing_total,
        'difference': (total_income - existing_total),
        'members_list': members_list,
        }

    

class MembersView(LoginRequiredMixin, SuccessMessageMixin,ListView):
    model = Member
    template_name = 'familyTrust/members/members.html'
    context_object_name = 'members'

class AddMemberView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    # Only Superuser can add members
    def test_func(self):
        return self.request.user.is_superuser

    form_class = MemberForm
    success_url = reverse_lazy('members')
    template_name = 'familyTrust/members/add-member.html'
    success_message = "تمت إضافة العضو بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateMemberView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    # Only Superuser can update accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Member
    form_class = UpdateMemberForm
    template_name = 'familyTrust/members/update-member.html'
    success_url = reverse_lazy('members')  # Redirect to accounts after successful update
    success_message = "تم  تعديل بيانات العضو بنجاح"
    #extra_context = {'member_username': 'This is some extra information'}

    # Define get_context_data to add extra context
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        member_username = get_object_or_404(Member, id=pk)
        context = super().get_context_data(**kwargs)
        context['member_username'] = member_username.member.username
        return context

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Member, id=pk)

class DeleteMemberView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    # Only Superuser can delete accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Member
    template_name = 'familyTrust/members/delete-member.html'
    success_url = reverse_lazy('members')  # Redirect to accounts after deletion
    success_message = "تم حذف العضو بنجاح."

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Member, id=pk)
    
############ Loan

class LoansView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Loan
    template_name = 'familyTrust/loans/loans.html'
    context_object_name = 'loans'

class AddLoanView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    # Only Superuser can add members
    def test_func(self):
        return self.request.user.is_superuser

    form_class = LoanForm
    success_url = reverse_lazy('loans')
    template_name = 'familyTrust/loans/add-loan.html'
    success_message = "تمت إضافة بيانات القرض بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateLoanView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Loan
    form_class = LoanForm
    template_name = 'familyTrust/loans/update-loan.html'
    success_url = reverse_lazy('loans')  # Redirect to loans after successful update
    success_message = "تم  تعديل البيانات بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the loan based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Loan, id=pk)

class DeleteLoanView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Loan
    template_name = 'familyTrust/loans/delete-loan.html'
    success_url = reverse_lazy('loans')  # Redirect to loans after deletion
    success_message = "تم حذف بيانات القرض بنجاح."

    def get_object(self, queryset=None):
        # Fetch the loan based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Loan, id=pk)

############ Investments

class InvestmentsView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Investment
    template_name = 'familyTrust/investments/investments.html'
    context_object_name = 'investments'

class AddInvestmentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    # Only Superuser can add members
    def test_func(self):
        return self.request.user.is_superuser

    form_class = InvestmentForm
    success_url = reverse_lazy('investments')
    template_name = 'familyTrust/investments/add-investment.html'
    success_message = "تمت إضافة بيانات الإستثمار بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateInvestmentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Investment
    form_class = InvestmentForm
    template_name = 'familyTrust/investments/update-investment.html'
    success_url = reverse_lazy('investments')  # Redirect to investments after successful update
    success_message = "تم  تعديل البيانات بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the investment based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Investment, id=pk)

class DeleteInvestmentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Investment
    template_name = 'familyTrust/investments/delete-investment.html'
    success_url = reverse_lazy('investments')  # Redirect to investments after deletion
    success_message = "تم حذف بيانات الإستثمار بنجاح."

    def get_object(self, queryset=None):
        # Fetch the investment based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Investment, id=pk)
    
############ Subscriptions

class SubscriptionsView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subscription
    template_name = 'familyTrust/subscriptions/subscriptions.html'
    context_object_name = 'subscriptions'

class AddSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    form_class = SubscriptionForm
    success_url = reverse_lazy('subscriptions')
    template_name = 'familyTrust/subscriptions/add-subscription.html'
    success_message = "تمت إضافة بيانات الاشتراك بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'familyTrust/subscriptions/update-subscription.html'
    success_url = reverse_lazy('subscriptions')  # Redirect to subscriptions after successful update
    success_message = "تم  تعديل البيانات بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the subscription based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Subscription, id=pk)

class DeleteSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Subscription
    template_name = 'familyTrust/subscriptions/delete-subscription.html'
    success_url = reverse_lazy('subscriptions')  # Redirect to subscriptions after deletion
    success_message = "تم حذف بيانات الاشتراك بنجاح."

    def get_object(self, queryset=None):
        # Fetch the subscription based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Subscription, id=pk)
    
############ Transaction

class TransactionsView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Transaction
    template_name = 'familyTrust/transactions/transactions.html'
    context_object_name = 'transactions'

class AddTransactionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    # Only Superuser can add members
    def test_func(self):
        return self.request.user.is_superuser

    form_class = TransactionForm
    success_url = reverse_lazy('transactions')
    template_name = 'familyTrust/transactions/add-transaction.html'
    success_message = "تمت إضافة الحوالة بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateTransactionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    # Only Superuser can update accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Transaction
    form_class = TransactionForm
    template_name = 'familyTrust/transactions/update-transaction.html'
    success_url = reverse_lazy('transactions')  # Redirect to accounts after successful update
    success_message = "تم  تعديل الحوالة بنجاح"

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Transaction, id=pk)

class DeleteTransactionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    # Only Superuser can delete accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Transaction
    template_name = 'familyTrust/transactions/delete-transaction.html'
    success_url = reverse_lazy('transactions')  # Redirect to accounts after deletion
    success_message = "تم حذف الحوالة بنجاح."

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Transaction, id=pk)