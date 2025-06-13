from django.urls import path
from .views import (CreateMailingRecipient, ListMailingRecipient, DetailMailingRecipient, UpdateMailingRecipient,
                    DeleteMailingRecipient, ListMessage, CreateMessage, DetailMessage, UpdateMessage, DeleteMessage)


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

]
