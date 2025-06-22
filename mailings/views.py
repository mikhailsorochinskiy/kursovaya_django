from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import MailingRecipient, Message, Mailing, TryMailing
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from config.settings import EMAIL_HOST_USER
from .services import send_mailing, message_count
from .forms import MailingRecipientForm, MessageForm, MailingForm


# Контроллеры для получателей
class ListMailingRecipient(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_list.html'
    context_object_name = 'mailing_recipients'

    @method_decorator(cache_page(60, key_prefix="mailings:mailing_recipients_list"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm('mailings.can_view_mailing_recipient'):
            return MailingRecipient.objects.all()
        return MailingRecipient.objects.filter(owner=self.request.user)


class CreateMailingRecipient(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailing_recipient/mailing_recipient_form.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMailingRecipient(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_detail.html'
    context_object_name = 'mailing_recipient'


class UpdateMailingRecipient(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailing_recipient/mailing_recipient_form.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingRecipientForm
        # if user.has_perm('catalog.can_unpublish_product') and user.has_perm('catalog.delete_product'):
        #     return ProductModeratorForm
        raise PermissionDenied


class DeleteMailingRecipient(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient/mailing_recipient_delete.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')
    context_object_name = 'mailing_recipient'

    def get_object(self, queryset=None):
        mailing_recipient = get_object_or_404(MailingRecipient, pk=self.kwargs["pk"])
        if mailing_recipient.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать получателя.")
        return mailing_recipient


# Контроллеры для сообщений
class ListMessage(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message/message_list.html'
    context_object_name = 'messages'

    @method_decorator(cache_page(60, key_prefix="mailings:messages_list"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CreateMessage(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message/message_form.html'
    success_url = reverse_lazy('mailings:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMessage(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message/message_detail.html'
    context_object_name = 'message'


class UpdateMessage(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message/message_form.html'
    success_url = reverse_lazy('mailings:messages_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        # if user.has_perm('catalog.can_unpublish_product') and user.has_perm('catalog.delete_product'):
        #     return ProductModeratorForm
        raise PermissionDenied


class DeleteMessage(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/message/message_delete.html'
    success_url = reverse_lazy('mailings:messages_list')
    context_object_name = 'message'

    def get_object(self, queryset=None):
        message = get_object_or_404(Message, pk=self.kwargs["pk"])
        if message.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать это сообщение.")
        return message


# Контролеры для рассылок
class ListMailing(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_list.html'
    context_object_name = 'mailings'

    @method_decorator(cache_page(60, key_prefix="mailings:mailings_list"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm('mailings.can_view_mailing'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class CreateMailing(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMailing(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class UpdateMailing(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        # if user.has_perm('catalog.can_unpublish_product') and user.has_perm('catalog.delete_product'):
        #     return ProductModeratorForm
        raise PermissionDenied


class DeleteMailing(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing/mailing_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        mailing = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if mailing.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать эту рассылку.")
        return mailing


class HomePage(ListView):
    model = Mailing
    template_name = 'mailings/home.html'
    context_object_name = 'mailing'

    @method_decorator(cache_page(60, key_prefix="mailings:home"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            mailings_started = self.get_queryset().filter(status='started')
            context['mailings_started_count'] = mailings_started.count()
            mailing_recipients = MailingRecipient.objects.filter(owner=self.request.user)
            context['mailing_recipients_count'] = mailing_recipients.count()
            return context


class ListTryMailing(LoginRequiredMixin, ListView):
    model = TryMailing
    template_name = 'mailings/try_mailing_list.html'
    context_object_name = 'try_mailings'

    @method_decorator(cache_page(60, key_prefix="mailings:try_mailings"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return TryMailing.objects.filter(owner=self.request.user)


class StatisticView(LoginRequiredMixin, ListView):
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
            if mailing.can_used:
                send_mailing(mailing_id, try_mailing)
                messages.success(request, f'Рассылка "{mailing.name}" успешно отправлена!')
                return redirect('mailings:mailings_list')
        except Exception as e:
            return HttpResponse(f'Расылка не удалась по причине: {e}')

    return redirect('mailings:mailing_detail', mailing_id=mailing_id)


def block_mailing_view(request, mailing_id):
    if request.user.has_perm('mailings.can_view_mailing'):
        if request.method == "POST":
            mailing = get_object_or_404(Mailing, id=mailing_id)
            if mailing.can_used:
                mailing.can_used = False
                mailing.save()
            else:
                mailing.can_used = True
                mailing.save()
            return redirect('mailings:mailings_list')
    raise PermissionDenied
