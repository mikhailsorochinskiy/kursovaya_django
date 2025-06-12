from django.db import models

# Create your models here.
class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    fio = models.CharField(verbose_name='ФИО', max_length=150, blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылок'


class Message(models.Model):
    message_topic = models.CharField(verbose_name='Тема сообщения', max_length=150, blank=True, null=True)
    message_text = models.TextField(verbose_name='Текст сообщения', blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('stopped', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    ]

    date_start = models.DateTimeField(auto_now_add=True, verbose_name='дата первой отправки')
    date_end = models.DateTimeField(auto_now=True, verbose_name='дата окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='messages')
    recipients = models.ManyToManyField(MailingRecipient)

    def __str__(self):
        return f'{self.message} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
