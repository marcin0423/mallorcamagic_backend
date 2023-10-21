from django.urls import path
from . import views
from . import api

urlpatterns = [
    # path('', views.test_index, name="property_index"),
    path('', api.get_property_detail, name="property_detail"),
    path('locations/', api.get_all_locations, name="all_location"),
    path('latest/', api.get_latest_property, name="property_latest"),
    path('search/', api.search_property, name="property_search"),
    path('gallery/', api.gallery_property, name="property_gallery"),
    path('top/', api.top_property, name="property_top"),
    path('map/', api.map_property, name="property_map"),
    path('total/', api.get_property_count, name="property_total"),
    path('agent/', api.agent_details, name="property_agent_detail"),
    path('agent/view/', api.increment_agent_views, name="increment_agent_view"),
    path('agent/property/', api.get_agent_property, name="property_agent_property"),
    path('contact/', api.SavePropertyContactRequest.as_view(), name="property_contact")
]
