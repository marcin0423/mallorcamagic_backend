from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def index(request):
    print(request.GET)
    print(settings.BASE_DIR / "res")
    return HttpResponse("Hey there, guide api is working...")
