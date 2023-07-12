import schedule
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from datetime import datetime, timedelta
from mailing_app.models import Mailing, MailingAttempt


def send_message(mail):
    status_list = []
    # Получить всех клиентов в рассылке
    mail_list = mail.clients.all()
    for client in mail_list:
        try:
            send_mail(subject=mail.message.subject,
                      message=mail.message.body,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[client.email],
                      fail_silently=False)
        except Exception as e:
            server_response = {'status': MailingAttempt.FAILED,
                               'server_response': 'Ошибка при отправке сообщения: {}'.format(str(e)),
                               'mailing': Mailing.objects.get(pk=mail.id)}
            status_list.append(MailingAttempt(**server_response))
        else:
            server_response = {'status': MailingAttempt.SENT,
                               'server_response': 'Сообщение успешно отправлено',
                               'mailing': Mailing.objects.get(pk=mail.id)}
            status_list.append(MailingAttempt(**server_response))

    MailingAttempt.objects.bulk_create(status_list)


def start_mailing():
    # Получить все рассылки
    mailings = Mailing.objects.all()
    print(mailings)
    for mailing in mailings:
        if mailing.mailing_status == Mailing.STARTED:
            obj = MailingAttempt.objects.filter(mailing=mailing).last()

            if obj is None:
                mail_time = mailing.mailing_time.replace(second=0, microsecond=0)
                now_time = datetime.now().time().replace(second=0, microsecond=0)
                if mail_time == now_time:
                    send_message(mailing)

            else:
                frequency = mailing.frequency
                obj_time = obj.time

                if frequency == Mailing.DAILY:
                    obj_time += timedelta(days=1)
                elif frequency == Mailing.WEEKLY:
                    obj_time += timedelta(days=7)
                elif frequency == Mailing.MONTHLY:
                    obj_time += timedelta(days=30)
                obj_time = obj_time.replace(second=0, microsecond=0)
                now_time = datetime.now().replace(second=0, microsecond=0)
                if obj_time == now_time:
                    send_message(mailing)


def run_scheduler():
    schedule.every(60).seconds.do(start_mailing)


def cache_message(model, key):
    queryset = model.objects.all()
    if settings.CACHE_ENABLED:
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
        return cache_data
    return queryset
