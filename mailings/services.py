from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Mailing, MailingRecipient, TryMailing
from config.settings import EMAIL_HOST_USER



def validate_mailing_time(mailing):
    "Проверка времени у рассылки"
    now = timezone.now()

    if mailing.status == "stopped":
        raise ValidationError("Рассылка завершена и ее нельзя повторно запустить")

    if mailing.date_start and now < mailing.date_start:
        raise ValidationError("Рассылка еще не началась")

    if mailing.date_end and now > mailing.date_end:
        mailing.status = "stopped"
        mailing.save()
        raise ValidationError("Рассылка уже завершена")

    if mailing.status != "started":
        mailing.status = "started"
        if not mailing.date_start:
            mailing.date_start = now
        mailing.save()


def send_mailing(mailing_id):
    """Отправка рассылки"""
    mailing = get_object_or_404(Mailing, id=mailing_id)
    validate_mailing_time(mailing)
    message = mailing.message
    recipients = mailing.recipients.all()
    try_mailing = TryMailing.objects.create(mailing=mailing)

    try:
        send_mail(subject=message.message_topic,
                  message=message.message_text,
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[recipient.email for recipient in recipients],
                  fail_silently=False,
                  )
        if mailing.date_end and timezone.now() > mailing.date_end:
            mailing.status = "stopped"
            mailing.save()
        try_mailing.status = 'successful'
        try_mailing.save()
        # messages.success(request, f'Рассылка "{message.message_topic}" успешно отправлена!')
        # return redirect('mailings:mailings_list')
    except Exception as e:
        try_mailing.status = 'no_successful'
        try_mailing.ans_from_email_server = f'Error sending mailing {mailing.id}: {str(e)}'
        try_mailing.save()
