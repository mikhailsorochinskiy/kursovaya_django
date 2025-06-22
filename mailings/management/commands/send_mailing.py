from django.core.management.base import BaseCommand
from mailings.models import Mailing, TryMailing
from django.utils import timezone
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'Send mailing'

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status="created")
        for mailing in mailings:
            try_mailing = TryMailing.objects.create(mailing=mailing)
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
