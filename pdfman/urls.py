from django.urls import path
from .views import *

urlpatterns = [
    path('', pdfman, name='pdfman'),
]