from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
# Customized
from .forms import RegisterForm


class AccountListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = 'home'