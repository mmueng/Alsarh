from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^/JoinThisOrder$', views.Join_order),
    url(r'^/assignThisOrder$', views.assign_order_to),
    url(r'^/new$', views.new),
    url(r'^/new/addcustomer$', views.add_customer),

    url(r'^/History$', views.Historyst),
    url(r'^/neworder$', views.new_order),
    url(r'^/(?P<orderID>\d+)/delete$', views.delete),
    url(r'^/(?P<orderID>\d+)/remove$', views.remove),
    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/remove2$', views.remove2),

    url(r'^/(?P<orderID>\d+)/return$', views.return_to_tasks),
    url(r'^/neworder/(?P<customerID>\d+)/show$', views.show),
    url(r'^/neworder/(?P<customerID>\d+)/edit$', views.edit),
    url(r'^/neworder/(?P<customerID>\d+)/edit/process$', views.edit_customer),
    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/show$', views.show_order),
    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/edit$', views.edit_order),

    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/postcomment$',
        views.post_comment),


    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/status$', views.status),
    url(r'^/neworder/(?P<customerID>\d+)/(?P<orderID>\d+)/process$',
        views.edit_order_process),
    url(r'^/neworder/(?P<customerID>\d+)/addorder$', views.add_order),
]
