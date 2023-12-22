from django.urls import path
from .views import *

urlpatterns = [
    path('', Trust.as_view(), name='trust'),
    path('members/', MembersView.as_view(), name='members'),
    path('members/add-member/', AddMemberView.as_view(), name='add-member'),
    path('members/update-member/<int:pk>/', UpdateMemberView.as_view(), name='update-member'),
    path('members/delete-member/<int:pk>/', DeleteMemberView.as_view(), name='delete-member'),
]