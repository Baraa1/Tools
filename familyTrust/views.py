from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .forms import *

class Trust(TemplateView):
    template_name = 'familyTrust/trust.html'

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