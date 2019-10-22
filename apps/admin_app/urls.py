from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^/new$', views.new),
    url(r'^/(?P<userID>\d+)/edit$', views.edit),
    url(r'^/(?P<userID>\d+)/processedit$', views.process_edit),
    url(r'^/(?P<userID>\d+)/delete$', views.delete),

]
