from django.urls import path, include

from backend import views as backend

urlpatterns = [
    path('whatsapp/', include([
        path('start/',
             backend.whatsapp.Start.as_view(),
             name='backend_whatsapp_start'),
        path('stop/',
             backend.whatsapp.Stop.as_view(),
             name='backend_whatsapp_stop'),
        path('save_messaging_settings/',
             backend.whatsapp.SaveMessagingSettings.as_view(),
             name='backend_whatsapp_save_messaging_settings'),
        path('clear_messaging_settings/',
             backend.whatsapp.ClearMessagingSettings.as_view(),
             name='backend_whatsapp_clear_messaging_settings'),
        path('send_debug_message/',
             backend.whatsapp.SendDebugMessage.as_view(),
             name='backend_whatsapp_send_debug_message'),
        path('update_qr_code/',
             backend.whatsapp.UpdateQrCode.as_view(),
             name='backend_whatsapp_update_qr_code'),
    ]))
]
