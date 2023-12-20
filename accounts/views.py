from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
# Customized
from .forms import *


class AccountListView(ListView):
    model = User
    template_name = 'accounts/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        """
        Return a filtered queryset based on some criteria.
        For example, return only non-staff users.
        """
        return User.objects.filter(is_superuser=False, is_staff=False)

class RegisterView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    # Only Superuser can create accounts
    def test_func(self):
        return self.request.user.is_superuser

    form_class = RegisterForm
    success_url = reverse_lazy('accounts')
    template_name = 'accounts/register.html'
    success_message = "The account was created successfully."

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    # Only Superuser can update accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = User
    form_class = AccountUpdateForm
    template_name = 'accounts/update-account.html'
    success_url = reverse_lazy('accounts')  # Redirect to accounts after successful update
    success_message = "The account was updated successfully."

    # This method is called if the form is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, id=pk)

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    # Only Superuser can delete accounts
    def test_func(self):
        return self.request.user.is_superuser
    
    model = User
    template_name = 'accounts/delete-account.html'
    success_url = reverse_lazy('accounts')  # Redirect to accounts after deletion
    success_message = "The account was deleted successfully."

    def get_object(self, queryset=None):
        # Fetch the user based on the ID from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, id=pk)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class CustomLogoutView(LogoutView):
    next_page = 'index'