from django.contrib import admin

from mailing_app.models import Message, Mailing, MailingAttempt, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comments',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_time', 'frequency', 'mailing_status', 'message')
    filter_horizontal = ('clients',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'time', 'status', 'server_response',)
    list_filter = ('status',)
