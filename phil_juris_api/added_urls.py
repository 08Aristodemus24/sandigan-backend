from django.urls import path
from . import views

app_name = 'phil_juris_api'

urlpatterns = [
    path('', views.index, name='testing_index')
]