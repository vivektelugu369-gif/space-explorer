from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('add_favourate/',add_favourate,name='add_favourate'),
    path('my_favourates/',my_favourates,name='my_favourates'),
    path('remove_favourate/<int:id>/',remove_favourate,name='remove_favourate'),
    path('about/',about,name='about')
]