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
        path('send/',
             backend.whatsapp.Send.as_view(),
             name='backend_whatsapp_send'),
        path('send_manual_message/',
             backend.whatsapp.SendManualMessage.as_view(),
             name='backend_whatsapp_send_manual_message'),
        path('prevent_selenium_session_timeout/',
             backend.whatsapp.PreventSeleniumSessionTimeout.as_view(),
             name='backend_whatsapp_prevent_selenium_session_timeout'),
    ])),
    path('deskmanager/', include([
        path('save_keys/',
             backend.deskmanager.SaveKeys.as_view(),
             name='backend_deskmanager_save_keys'),
        path('clear_keys/',
             backend.deskmanager.ClearKeys.as_view(),
             name='backend_deskmanager_clear_keys'),
        path('set_data_update_mode/',
             backend.deskmanager.SetDataUpdateMode.as_view(),
             name='backend_deskmanager_set_data_update_mode'),
        path('clear_messaging_settings/',
             backend.deskmanager.ClearDataUpdateMode.as_view(),
             name='backend_deskmanager_clear_data_update_mode'),
        path('update_data/',
             backend.deskmanager.UpdateData.as_view(),
             name='backend_deskmanager_update_data'),
    ])),
]
