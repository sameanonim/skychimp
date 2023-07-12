from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=50, verbose_name='контактный email', unique=True)
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comments = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело сообщения')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    FREQUENCY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно')
    ]
    CREATED = 'created'
    STARTED = 'started'
    FINISHED = 'finished'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена')
    ]
    mailing_time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=50, verbose_name='Периодичность', choices=FREQUENCY_CHOICES, default=DAILY)
    mailing_status = models.CharField(max_length=50, verbose_name='Статус рассылки', choices=STATUS_CHOICES,
                                      default=CREATED)

    clients = models.ManyToManyField(Client, verbose_name='Клиенты для рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема письма')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'ID: {self.id} - время рассылки: {self.mailing_time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'set_mailing_status',
                'Can set mailing status'
            ),
        ]


class MailingAttempt(models.Model):
    SENT = 'sent'
    FAILED = 'failed'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (SENT, 'Отправлено'),
        (FAILED, 'Не удалось отправить'),
        (PENDING, 'В ожидании')
    ]
    time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='статус попытки', choices=STATUS_CHOICES, default=PENDING)
    server_response = models.CharField(**NULLABLE, max_length=150, verbose_name='ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
