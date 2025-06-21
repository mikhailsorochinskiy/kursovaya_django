from django import forms
from .models import MailingRecipient, Message, Mailing


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['fio', 'email','comment',]

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
        fields = ['name', 'message', 'recipients',]

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя рассылки'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите сообщение из предложенного списка'
        })

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите список получателей рассылки'
        })
