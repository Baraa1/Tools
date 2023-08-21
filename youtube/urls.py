from django.urls import path
from .views import *

urlpatterns = [
    path('', youtube, name='youtube'),
    path('get_video/', get_video, name='get_video'),
    path('download_links/', download_links, name='download_links')
    #path('download_video/', download_video, name='download_video'),
    #path('serve_file/', serve_file, name='serve_file'),
]