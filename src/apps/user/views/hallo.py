from django.shortcuts import HttpResponse

# Create your views here.
def hallo(request):
    return HttpResponse("hallo")