from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register_user$', views.register_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]