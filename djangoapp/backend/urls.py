from django.urls import path, include

from backend.views import whatsapp

urlpatterns = [
    path('whatsapp/', include([
        path('start/', whatsapp.Start.as_view(), name='start_wa'),
        path('stop/', whatsapp.Stop.as_view(), name='stop_wa'),
        path('save_messaging_settings/', whatsapp.SaveMessagingSettings.as_view(),
             name='save_messaging_settings'),
        path('clear_messaging_settings/', whatsapp.ClearMessagingSettings.as_view(),
             name='clear_messaging_settings'),
        path('send_message/', whatsapp.SendDebugMessage.as_view(),
             name='send_message'),
        path('update_qr_code/', whatsapp.UpdateQrCode.as_view(),
             name='update_qr_code'),
    ])),

]
