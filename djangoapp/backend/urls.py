from django.urls import path, include

from . import views

urlpatterns = [
    path('whatsapp/', include([
        path('start/', views.start_wa, name='start_wa'),
        path('stop/', views.stop_wa, name='stop_wa'),
        path('save_messaging_settings/', views.save_messaging_settings,
             name='save_messaging_settings'),
        path('clear_messaging_settings/', views.clear_messaging_settings,
             name='clear_messaging_settings'),
        path('send_message/', views.send_debug_message,
             name='send_message'),
    ])),

]
