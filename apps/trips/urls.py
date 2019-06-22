from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^(?P<trip_id>\d+)$', views.trip_info),
    url(r'^edit/(?P<trip_id>\d+)$', views.edit),
    url(r'^new$', views.new),
    url(r'^create_trip$', views.create_trip),
    url(r'^remove/(?P<trip_id>\d+)$', views.remove),
    url(r'^update/(?P<trip_id>\d+)$', views.update_trip),
    url(r'^cancel/(?P<joined_id>\d+)$', views.cancel_joined),
    url(r'^join/(?P<join_id>\d+)$', views.join_trip),
]