from django.urls import path
from .views import *

urlpatterns = [
    path('users/', AccountListView.as_view(), name='user_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]