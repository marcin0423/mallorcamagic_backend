from django.urls import path
from . import api

urlpatterns = [
    # path('', views.test_index, name="property_index"),
    path('', api.get_contents, name="all_contents"),
]
