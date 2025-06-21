from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Mailing, MailingRecipient, TryMailing
from config.settings import EMAIL_HOST_USER


def validate_mailing_status(mailing):
    "Проверка времени у рассылки"

    if mailing.status == 'started':
        raise ValidationError('Рассылка уже запущена')

    mailing.status = "started"
    mailing.save()


def send_mailing(mailing_id, try_mailing):
    """Отправка рассылки"""
    mailing = get_object_or_404(Mailing, id=mailing_id)
    validate_mailing_status(mailing)
    mailing.date_start = timezone.now()
    message = mailing.message
    recipients = mailing.recipients.all()

    try:
        send_mail(subject=message.message_topic,
                  message=message.message_text,
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[recipient.email for recipient in recipients],
                  fail_silently=False,
                  )

        try_mailing.status = 'successful'
        try_mailing.save()

    except Exception as e:
        try_mailing.status = 'no_successful'
        try_mailing.ans_from_email_server = f'Error sending mailing {mailing.id}: {str(e)}'
        try_mailing.save()
    finally:
        mailing.date_end = timezone.now()
        mailing.status = "stopped"
        mailing.save()


def message_count(try_mailings):
    count = 0
    for try_mailing in try_mailings:
        count += try_mailing.mailing.recipients.count()
    return count
