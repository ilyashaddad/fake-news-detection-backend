from django.urls import path
from . import views
from graphene_django.views import GraphQLView
# User url

urlpatterns=[
    path('',views.user),
    path('hallo/',views.hallo)
]