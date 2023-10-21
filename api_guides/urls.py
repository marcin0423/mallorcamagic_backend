from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', api.get_guide_with_slug, name="guide_single"),
    path('latest/', api.get_latest_guides, name="guide_latest"),
    path('search/', api.search_guides, name="guide_search"),
    path('suggestion/', api.get_suggested_guides, name="guide_suggestion"),
    path('bot_handler/', api.bot_email_collector_handler, name="bot_handler"),
]
