from django.apps import AppConfig


class MailingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_app'
    verbose_name = 'сервис управления рассылками'
