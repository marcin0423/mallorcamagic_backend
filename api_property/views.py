from django.http import HttpResponse


def test_index(request):
    return HttpResponse("Hey there, property app is working")
