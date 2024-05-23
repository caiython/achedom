from django.urls import path

from app.views import *

urlpatterns = [
    path('welcome/', Welcome.as_view(), name='welcome'),
    path('', Home.as_view(), name='home'),
    path('service_orders/', ServiceOrders.as_view(), name='service_orders'),
    path('config/', Config.as_view(), name='config'),
    path('celery_hello_world/', CeleryHelloWorld.as_view(),
         name='celery_hello_world')
]
