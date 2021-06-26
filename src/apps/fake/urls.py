from django.urls import path
from . import views
from graphene_django.views import GraphQLView
from .schema import schema
# User url

urlpatterns=[
    path('',GraphQLView.as_view(graphiql=True,schema=schema))
]