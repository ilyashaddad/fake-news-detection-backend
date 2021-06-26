from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import HttpResponse
# Create your views here.
def Fake(request):
    return JsonResponse({
            "hallo":"qhsqjsqh"
        })
