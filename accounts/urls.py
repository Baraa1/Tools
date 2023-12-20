from django.urls import path
from .views import *

urlpatterns = [
    path('', AccountListView.as_view(), name='accounts'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account-update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
    path('account-delete/<int:pk>/', AccountDeleteView.as_view(), name='account-delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]