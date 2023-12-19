from django.urls import path
from .views import *

urlpatterns = [
    path('', Trust.as_view(), name='trust'),
]