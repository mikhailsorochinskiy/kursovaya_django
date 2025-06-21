from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import MailingRecipient, Message, Mailing, TryMailing
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from .services import send_mailing, message_count
from .forms import MailingRecipientForm, MessageForm, MailingForm


# Контроллеры для получателей
class ListMailingRecipient(ListView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_list.html'
    context_object_name = 'mailing_recipients'


class CreateMailingRecipient(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailing_recipient/mailing_recipient_form.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMailingRecipient(DetailView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_detail.html'
    context_object_name = 'mailing_recipient'


class UpdateMailingRecipient(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
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
    form_class = MessageForm
    template_name = 'mailings/message/message_form.html'
    success_url = reverse_lazy('mailings:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMessage(DetailView):
    model = Message
    template_name = 'mailings/message/message_detail.html'
    context_object_name = 'message'


class UpdateMessage(UpdateView):
    model = Message
    form_class = MessageForm
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
    form_class = MailingForm
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMailing(DetailView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class UpdateMailing(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')


class DeleteMailing(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')
    context_object_name = 'mailing'


class HomePage(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/home.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings_started = self.get_queryset().filter(status='started')
        context['mailings_started_count'] = mailings_started.count()
        mailing_recipients = MailingRecipient.objects.filter(owner=self.request.user)
        context['mailing_recipients_count'] = mailing_recipients.count()
        return context


class ListTryMailing(ListView):
    model = TryMailing
    template_name = 'mailings/try_mailing_list.html'
    context_object_name = 'try_mailings'


class StatisticView(ListView):
    model = TryMailing
    template_name = 'mailings/statistic.html'
    context_object_name = 'try_mailings'

    def get_queryset(self):
        return TryMailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        successful_try = self.get_queryset().filter(status='successful')
        no_successful_try = self.get_queryset().filter(status='no_successful')
        messages_count = message_count(self.get_queryset())
        context['successful_try'] = successful_try.count()
        context['no_successful_try'] = no_successful_try.count()
        context['messages_count'] = messages_count
        return context


def send_mailing_view(request, mailing_id):
    if request.method == "POST":
        mailing = get_object_or_404(Mailing, id=mailing_id)
        try_mailing = TryMailing.objects.create(mailing=mailing)
        try_mailing.owner = request.user
        try:
            send_mailing(mailing_id, try_mailing)
            messages.success(request, f'Рассылка "{mailing.name}" успешно отправлена!')
            return redirect('mailings:mailings_list')
        except Exception as e:
            return HttpResponse(f'Раасылка не удалась по причине: {e}')

    return redirect('mailings:mailing_detail', mailing_id=mailing_id)
