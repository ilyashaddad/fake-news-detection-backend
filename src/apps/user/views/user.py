from django.shortcuts import HttpResponse

# Create your views here.
def user(request):
    return HttpResponse("hallo user")