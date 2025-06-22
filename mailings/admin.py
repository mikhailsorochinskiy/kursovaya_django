from django.contrib import admin
from .models import MailingRecipient, Message, Mailing, TryMailing


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fio')
    search_fields = ('email', 'fio')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_topic')
    search_fields = ('message_topic',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name', 'status')


@admin.register(TryMailing)
class TryMailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date')
    search_fields = ('status', )
