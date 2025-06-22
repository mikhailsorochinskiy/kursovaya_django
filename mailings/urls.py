from django.urls import path
from .views import (CreateMailingRecipient, ListMailingRecipient, DetailMailingRecipient, UpdateMailingRecipient,
                    DeleteMailingRecipient, ListMessage, CreateMessage, DetailMessage, UpdateMessage, DeleteMessage,
                    ListMailing, CreateMailing, UpdateMailing, DetailMailing, DeleteMailing, send_mailing_view, HomePage,
                    ListTryMailing, StatisticView, block_mailing_view)


app_name = 'mailings'

urlpatterns = [
    path('mailing_recipient/create/', CreateMailingRecipient.as_view(), name='mailing_recipient_create'),
    path('mailing_recipients/', ListMailingRecipient.as_view(), name='mailing_recipients_list'),
    path('mailing_recipient/<int:pk>', DetailMailingRecipient.as_view(), name='mailing_recipient_detail'),
    path('mailing_recipient/update/<int:pk>', UpdateMailingRecipient.as_view(), name='mailing_recipient_update'),
    path('mailing_recipient/delete/<int:pk>', DeleteMailingRecipient.as_view(), name='mailing_recipient_delete'),
    path('messages/', ListMessage.as_view(), name='messages_list'),
    path('message/create/', CreateMessage.as_view(), name='message_create'),
    path('message/<int:pk>', DetailMessage.as_view(), name='message_detail'),
    path('message/update/<int:pk>', UpdateMessage.as_view(), name='message_update'),
    path('message/delete/<int:pk>', DeleteMessage.as_view(), name='message_delete'),
    path('mailing/create/', CreateMailing.as_view(), name='mailing_create'),
    path('mailings/', ListMailing.as_view(), name='mailings_list'),
    path('mailing/<int:pk>', DetailMailing.as_view(), name='mailing_detail'),
    path('mailing/update/<int:pk>', UpdateMailing.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>', DeleteMailing.as_view(), name='mailing_delete'),
    path('mailing/<int:mailing_id>/send/', send_mailing_view, name='send_mailing'),
    path('home/', HomePage.as_view(), name='home'),
    path('try_mailings/', ListTryMailing.as_view(), name='try_mailings'),
    path('try_mailings/statistic/', StatisticView.as_view(), name='statistic'),
    path('mailing/<int:mailing_id>/can_used/', block_mailing_view, name='block_mailing'),
]
