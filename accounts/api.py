from multiprocessing import context
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import CustomUser
from FirebaseUtil.FirebaseAccountHelper import subscribe_user, save_or_update_user
import re
from utils.Common import verify_recaptcha_token_from_request
from rest_framework.authtoken.views import ObtainAuthToken
import requests
from utils.Logger import log
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.template.loader import get_template
import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone


def is_valid_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(pat, email):
        return True
    return False


def __send_vboat_request(email, fullname):
    try:
        url = "https://api.vbout.com/1/emailmarketing/addcontact.json?key=8628604507672758562277240"
        payload = {
            'status': 'disactive',
            'listid': '74936',
            'email': email,
            'fullname': fullname
        }
        files = []
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        log.debug(response.text)
    except Exception as e:
        log.error(str(e))


def __send_verification_email(email):
    # jwt token with 24 hours of expiration
    exp = datetime.now(tz=timezone.utc) + timedelta(hours=24)
    token = jwt.encode({"email": email, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")

    email_subject = "Please verify your email"
    email_body = get_template("emails/verify-email.html").render({
        "url": "https://mallorca-magic.com/verify-email?token=" + token,
        "hostname": "https://mallorca-magic.com"
    })
    try:
        send_mail(email_subject, email_body, 'info@mallorcamagic.es', [email], html_message=email_body)
    except Exception as e:
        log.error("Unable to send email verification mail: " + str(e))


# Get logged in user details
class LoggedInUser(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': "Not logged in user"}, status=status.HTTP_401_UNAUTHORIZED)
        loggedUser = UserSerializer(request.user)
        return Response(loggedUser.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_up_user(request):
    if 'username' not in request.data.keys():
        return Response({'error': "user name is required"}, status=status.HTTP_400_BAD_REQUEST)

    if 'password' in request.data.keys() and 'confirm' in request.data.keys():
        if request.data['password'] != request.data['confirm'] or len(request.data['password']) < 5:
            return Response({'error': "Password mismatch or too short"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': "Provide password and confirm password"}, status=status.HTTP_400_BAD_REQUEST)

    if 'email' in request.data.keys():
        if not is_valid_email(request.data['email']):
            return Response({'error': "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

    if not verify_recaptcha_token_from_request(request):
        return Response({'error': "Recaptcha token verification failed "}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email__iexact=request.data['email'])
        return Response({'error': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except: pass

    # create the user
    user = CustomUser(username=request.data['username'], email=request.data['email'])
    user.set_password(request.data['password'])
    user.save()

    # Save to firebase
    user_data = UserSerializer(user).data
    save_or_update_user(user_data)
    __send_vboat_request(user.email, user.username)
    __send_verification_email(user.email)

    # generate token
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token[0].key})


@api_view(['POST'])
def verify_email(request):
    if 'token' not in request.data.keys():
        return Response({'error': "token is required"}, status=status.HTTP_400_BAD_REQUEST)

    # verify the token
    token = request.data.get("token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        user = CustomUser.objects.get(email__iexact=payload['email'])
        user.is_verified = True
        user.save()
        return Response({'success': "Email successfully verified"}, status=status.HTTP_200_OK)
    except Exception as e:
        log.error(str(e))
        return Response({'error': "Verification token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def subscribe_news_letters(request):
    if 'email' in request.data.keys():
        if not is_valid_email(request.data['email']):
            return Response({'error': "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': "Please provide an email"}, status=status.HTTP_400_BAD_REQUEST)

    if not verify_recaptcha_token_from_request(request):
        return Response({'error': "Captcha verification is failed"}, status=status.HTTP_400_BAD_REQUEST)

    subscriber = subscribe_user(request.data['email'])
    return Response(subscriber, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request):
    if not request.user.is_authenticated:
        return Response({'error': "Login first"}, status=status.HTTP_400_BAD_REQUEST)

    if 'current_password' in request.data.keys():
        password = request.data['current_password']
        if not request.user.check_password(password):
            return Response({'error': "Current password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': "Please provide current password"}, status=status.HTTP_400_BAD_REQUEST)

    if 'password' in request.data.keys() and 'confirm' in request.data.keys():
        if request.data['password'] != request.data['confirm'] or len(request.data['password']) < 5:
            return Response({'error': "Password mismatch or too short"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': "Provide password and confirm password"}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(request.data['password'])
    request.user.save()
    return Response({'msg': "Successfully updated password"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_user_info(request):
    print(request.data)
    user = request.user
    if not user.is_authenticated:
        return Response({'error': "Login required"}, status=status.HTTP_400_BAD_REQUEST)

    if 'username' in request.data.keys():
        user.username = request.data['username']

    if 'news_letters' in request.data.keys():
        user.news_letters = request.data['news_letters']

    if 'guide_alert' in request.data.keys():
        user.guide_alert = request.data['guide_alert']

    if 'offers_alert' in request.data.keys():
        user.offers_alert = request.data['offers_alert']

    # Update user and save to firebase
    user.save()
    user_data = UserSerializer(user).data
    save_or_update_user(user_data)

    # generate token
    token = Token.objects.get_or_create(user=user)
    return Response(user_data, status=status.HTTP_200_OK)


# logged in override
class CustomObtainToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        if not verify_recaptcha_token_from_request(request):
            return Response({'error': "Captcha verification is failed"}, status=status.HTTP_400_BAD_REQUEST)

        # check if verified
        try:
            user = CustomUser.objects.get(email__iexact=request.data['username'])
            if not user.is_verified:
                return Response({'error': "Email is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        return super().post(request, *args, **kwargs)


# Reset password email
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    user = reset_password_token.user
    email_subject = "Reset your password"
    email_body = get_template("emails/forget-password.html").render({
        "reset_url": "https://mallorca-magic.com/reset-password?token=" + reset_password_token.key,
        "hostname": "https://mallorca-magic.com"
    })

    try:
        send_mail(email_subject, email_body, 'info@mallorcamagic.es',
                  [reset_password_token.user.email], html_message=email_body)
        log.debug("Successfully send password reset email")
    except Exception as e:
        log.error("Unable to send password reset mail: " + str(e))


@api_view(['POST'])
def contact_form(request):
    if not verify_recaptcha_token_from_request(request):
        return Response({'error': "Recaptcha token verification failed "}, status=status.HTTP_400_BAD_REQUEST)

    if 'email' in request.data.keys():
        if not is_valid_email(request.data['email']):
            return Response({'error': "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': "Please provide an email"}, status=status.HTTP_400_BAD_REQUEST)

    if "message" not in request.data.keys() or len(request.data['message']) <= 0:
        return Response({'error': "Please provide a message"}, status=status.HTTP_400_BAD_REQUEST)

    # submit here
    try:
        url = "https://www.vbt.io/embedcode/submit/74937/"
        payload = {
            'vbout_EmbedForm[field][408613]': request.data['name'],
            'vbout_EmbedForm[field][408616]': request.data['email'],
            'vbout_EmbedForm[field][408617]': request.data['phone'],
            'vbout_EmbedForm[field][408629]': request.data['message'],
            '_format': 'json'
        }
        response = requests.request("POST", url, data=payload)
        log.debug(response.text)
        return Response({'success': True}, status=status.HTTP_200_OK)
    except Exception as e:
        log.error(str(e))
        return Response({'error': "Something went wrong. Please try again later"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def test_email(request):
#     # render template
#     from django.shortcuts import render
#     context = {
#         "url": "https://mallorca-magic.com/verify-email?token=" + "12312312",
#         "hostname": "https://mallorca-magic.com"
#     }
#     return render(request, "emails/verify-email.html", context)
