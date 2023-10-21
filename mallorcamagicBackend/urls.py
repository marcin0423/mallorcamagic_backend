"""mallorcamagicBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="HelloHere API",
        default_version='v1',
        description="This is the HelloHere API Description",
        terms_of_service="https://www.mallorca-magic.com/terms-conditions",
        contact=openapi.Contact(email="info@hellohere.es"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/accounts/", include("accounts.urls")),
    path("api/saved/", include("saved_data.urls")),
    path("api/guide/", include("api_guides.urls")),
    path("api/property/", include("api_property.urls")),
    path("api/saved/", include("saved_data.urls")),
    path("api/activities/", include("api_activities.urls")),
    path("api/content/", include("api_content.urls")),
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    # path('admin/', admin.site.urls),
    # re_path(".*", TemplateView.as_view(template_name="index.html")),
]
