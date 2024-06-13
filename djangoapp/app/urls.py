from django.urls import path, re_path

from app.views import *

urlpatterns = [
    path('welcome/', Welcome.as_view(), name='welcome'),
    path('', Home.as_view(), name='home'),
    re_path(r'^service_orders/(?:(?P<page_number>\d+)/)?$',
            ServiceOrders.as_view(), name='service_orders'),
    path('config/', Config.as_view(), name='config'),
]
