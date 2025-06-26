from django import forms
from .models import MailingRecipient, Message, Mailing


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['fio', 'email', 'comment']

    def __init__(self, *args, **kwargs):
        super(MailingRecipientForm, self).__init__(*args, **kwargs)
        self.fields['fio'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ФИО'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Комментарий о получателе'
        })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_topic', 'message_text',]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['message_topic'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['message_text'].widget.attrs.update({
            'class': 'form-control',
        })


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'message', 'recipients']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов полей
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя рассылки'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите сообщение'
        })
        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите получателей'
        })

        # Фильтрация получателей и сообщений
        if self.user:
            if self.user.is_superuser:
                # Админ видит всех получателей
                recipients_queryset = MailingRecipient.objects.all()
                messages_queryset = Message.objects.all()
            else:
                # Обычный пользователь видит только своих
                recipients_queryset = MailingRecipient.objects.filter(owner=self.user)
                messages_queryset = Message.objects.filter(owner=self.user)

            self.fields['recipients'].queryset = recipients_queryset
            self.fields['message'].queryset = messages_queryset
