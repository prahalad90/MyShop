from django.urls import path, re_path
from blogs import views

urlpatterns = [
    path('',views.index,name='home')
]