from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import MailingRecipient, Message
from django.urls import reverse_lazy


#Контроллеры для получателей
class ListMailingRecipient(ListView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_list.html'
    context_object_name = 'mailing_recipients'


class CreateMailingRecipient(CreateView):
    model = MailingRecipient
    fields = ('email', 'fio', 'comment')
    template_name = 'mailings/mailing_recipient/mailing_recipient_form.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')


class DetailMailingRecipient(DetailView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_detail.html'
    context_object_name = 'mailing_recipient'


class UpdateMailingRecipient(UpdateView):
    model = MailingRecipient
    fields = ('email', 'fio', 'comment')
    template_name = 'mailings/mailing_recipient/mailing_recipient_form.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')


class DeleteMailingRecipient(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_delete.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')
    context_object_name = 'mailing_recipient'


#Контроллеры для сообщений
class ListMessage(ListView):
    model = Message
    template_name = 'mailings/message/message_list.html'
    context_object_name = 'messages'


class CreateMessage(CreateView):
    model = Message
    fields = ('message_topic', 'message_text')
    template_name = 'mailings/message/message_form.html'
    success_url = reverse_lazy('mailings:messages_list')


class DetailMessage(DetailView):
    model = Message
    template_name = 'mailings/message/message_detail.html'
    context_object_name = 'message'


class UpdateMessage(UpdateView):
    model = Message
    fields = ('message_topic', 'message_text')
    template_name = 'mailings/message/message_form.html'
    success_url = reverse_lazy('mailings:messages_list')


class DeleteMessage(DeleteView):
    model = Message
    template_name = 'mailings/message/message_delete.html'
    success_url = reverse_lazy('mailings:messages_list')
    context_object_name = 'message'
