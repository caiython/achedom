from django.urls import path

from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('', views.home, name='home'),
    path('service_orders/', views.service_orders, name='service_orders'),
    path('config/', views.config, name='config'),
    path('celery_hello_world/', views.celery_hello_world, name='celery_hello_world')
]
