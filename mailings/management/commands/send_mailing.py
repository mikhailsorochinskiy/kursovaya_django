from django.core.management.base import BaseCommand
from mailings.models import Mailing
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'Send mailing'

    def handle(self, *args, **options):
        # Получаем все рассылки, которые нужно отправить
        mailings = Mailing.objects.filter(status='created')  # предполагаем наличие поля is_sent

        if not mailings.exists():
            self.stdout.write(self.style.SUCCESS('No pending mailings to send.'))
            return

        for mailing in mailings:
            self.stdout.write(f'Processing mailing ID {mailing.id}...')

            message = mailing.message
            recipients = mailing.recipients.all()

            if not recipients.exists():
                self.stdout.write(self.style.WARNING(f'Mailing {mailing.id} has no recipients!'))
                continue

            try:
                for recipient in recipients:
                    send_mail(
                        message.message_topic,
                        message.message_text,
                        EMAIL_HOST_USER,
                        [recipient.email],
                        fail_silently=False,
                    )
                    self.stdout.write(f'Sent to {recipient.email}')

                mailing.status = 'started'
                mailing.save()
                self.stdout.write(self.style.SUCCESS(f'Mailing {mailing.id} sent successfully!'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error sending mailing {mailing.id}: {str(e)}'))
