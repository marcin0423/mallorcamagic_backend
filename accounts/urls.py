from django.urls import path, include
from . import api

urlpatterns = [
    path('login/', api.CustomObtainToken.as_view(), name="login"),
    path('user/', api.LoggedInUser.as_view(), name="user"),
    path('signup/', api.sign_up_user, name="signup"),
    path('subscribe/', api.subscribe_news_letters, name="subscribe"),
    path('change-pass/', api.change_password, name="change_pass"),
    path('update/', api.update_user_info, name="update"),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('verify-email/', api.verify_email, name="email_verification"),
    path('contact/', api.contact_form, name="contact_form"),
    # path('test-email/', api.test_email, name="test_email"),
]
