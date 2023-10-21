from django.urls import path
from . import api

urlpatterns = [
    path('', api.get_activities, name='activities'),
    path('activity/', api.get_activity_detail, name='activity_detail'),
    path('home/', api.get_home_activities, name='home_activties')
]
