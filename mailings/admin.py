from django.contrib import admin
from .models import MailingRecipient, Message, Mailing, TryMailing

# Register your models here.
@admin.register(MailingRecipient)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fio')
    search_fields = ('email', 'fio')


@admin.register(Message)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_topic')
    search_fields = ('message_topic',)


@admin.register(Mailing)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name', 'status')


@admin.register(TryMailing)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    search_fields = ('status', )
