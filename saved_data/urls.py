from django.urls import path
from . import api_views

urlpatterns = [
    path('guide/', api_views.SavedGuideEndpoint.as_view(), name="save_guide"),
    path('guide/get/', api_views.SavedGuideList.as_view(), name="save_guides"),
    path('property/', api_views.SavedPropertyEndpoint.as_view(), name="save_property"),
    path('property/get/', api_views.SavedPropertyList.as_view(), name="save_properties")
]
