from django.db import models
from users.models import User


# Create your models here.
class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    fio = models.CharField(verbose_name='ФИО', max_length=150, blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылок'


class Message(models.Model):
    message_topic = models.CharField(verbose_name='Тема сообщения', max_length=150, blank=True, null=True)
    message_text = models.TextField(verbose_name='Текст сообщения', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message_topic}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('stopped', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    ]
    name = models.CharField(max_length=50, verbose_name='Название рассылки', blank=True, null=True)
    date_start = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True, null=True, )
    date_end = models.DateTimeField(verbose_name="Дата и время окончания отправки", blank=True, null=True)


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='messages')
    recipients = models.ManyToManyField(MailingRecipient)
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class TryMailing(models.Model):
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('no_successful', 'Не успешно'),
    ]

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки отправки')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    ans_from_email_server = models.TextField(verbose_name='Ответ почтового сервера', blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
