from django.core.management.base import BaseCommand
from mailings.models import Mailing
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from mailings.services import send_mailing


class Command(BaseCommand):
    help = 'Send mailing'

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status="started",)
        for mailing in mailings:
            send_mailing(mailing.id)
