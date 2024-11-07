from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import send_mailing, IndexListView, MailingListView, MailingDetailView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingLogListView, \
    MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView, ClientListView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_log_list', MailingLogListView.as_view(), name='mailing_log_list'),
]
