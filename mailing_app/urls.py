from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_app.apps import MailingAppConfig
from mailing_app.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, MailingAttemptListView, set_mailing_status, HomePageView

app_name = MailingAppConfig.name

urlpatterns = [
    path('', cache_page(60)(HomePageView.as_view()), name='home'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_attempt_list/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
    path('set_mailing_status/<int:pk>', login_required(set_mailing_status), name='set_mailing_status')
]
