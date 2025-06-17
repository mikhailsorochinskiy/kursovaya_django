from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import MailingRecipient, Message, Mailing, TryMailing
from django.urls import reverse_lazy
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from .services import send_mailing


# Контроллеры для получателей
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


# Контроллеры для сообщений
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


# Контролеры для рассылок
class ListMailing(ListView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_list.html'
    context_object_name = 'mailings'


class CreateMailing(CreateView):
    model = Mailing
    fields = ('name', 'message', 'recipients', 'date_start', 'date_end')
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')


class DetailMailing(DetailView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class UpdateMailing(UpdateView):
    model = Mailing
    fields = ('status', 'message', 'recipients')
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')


class DeleteMailing(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')
    context_object_name = 'mailing'


class HomePage(ListView):
    model = Mailing
    template_name = 'mailings/home.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings_started = Mailing.objects.filter(status='started')
        context['mailings_started_count'] = mailings_started.count()
        mailing_recipients = MailingRecipient.objects.all()
        context['mailing_recipients_count'] = mailing_recipients.count()
        return context


class ListTryMailing(ListView):
    model = TryMailing
    template_name = 'mailings/try_mailing_list.html'
    context_object_name = 'try_mailings'


def send_mailing_view(request, mailing_id):
    if request.method == "POST":
        mailing = get_object_or_404(Mailing, id=mailing_id)
        try:
            send_mailing(mailing_id)
            messages.success(request, f'Рассылка "{mailing.name}" успешно отправлена!')
            return redirect('mailings:mailings_list')
        except Exception as e:
            return HttpResponse(f'Раасылка не удалась по причине: {e}')

    return redirect('mailings:mailing_detail', mailing_id=mailing_id)
