from django.urls import path

from . import views

urlpatterns = [
    path('start_wa/', views.start_wa, name='start_wa'),
]
