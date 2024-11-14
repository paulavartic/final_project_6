import random
from time import sleep

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.management import call_command
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone

import smtplib

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import ClientForm, MailingForm, MessageForm, MailingUpdateForm, MailingManagerUpdateForm
from mailing.models import MailingSettings, SendingAttempt, Client, Message
from mailing.services import get_mailing_from_cache, get_messages_from_cache


@login_required
def send_mailing(request):
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = timezone.now().astimezone(zone)

    mailings = MailingSettings.objects.filter(owner=request.user, first_send__lte=current_datetime)

    for mailing in mailings:
        for client in mailings.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )

                #Register successful operation
                attempt = SendingAttempt.objects.create(
                    mailing=mailing,
                    status='success',
                    server_response='Message sent at' + str(timezone.now())
                )
                attempt.save()
            except smtplib.SMTPException as e:
                #Register unsuccessful operation
                attempt = SendingAttempt.objects.create(
                    mailing=mailing,
                    status='failure',
                    server_response='Failed to send message:' + str(e)
                )
                attempt.save()

        #Updating mailing status
        mailing.status = 'running'
        mailing.save()


scheduler = BackgroundScheduler()
scheduler.add_job(send_mailing, 'interval', seconds=600)
scheduler.start()


class IndexListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'object_list'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings_count = len(MailingSettings.objects.all())
        mailings_is_active_count = len(MailingSettings.objects.filter(status='running'))
        unique_clients_count = Client.objects.values('email').distinct().count()
        context['mailings_count'] = mailings_count
        context['mailings_is_active_count'] = mailings_is_active_count
        context['unique_clients_count'] = unique_clients_count
        return context


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'object_list'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    context_object_name = 'object_list'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    template_name = 'mailing/client_delete.html'
    success_url = reverse_lazy('mailing/client_list')


class MailingCreateView(CreateView, LoginRequiredMixin):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get(self, request, **kwargs):
        form = self.form_class(self.request.user, request.POST)
        return render(request, 'mailing/mailing_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            clients = form.cleaned_data.get('clients')
            if not clients:
                form.add_error('clients', 'Choose one client.')
            mailing = form.save(commit=False)
            mailing.user = self.request.user
            mailing.save()
            form.save_m2m()
            return redirect(self.success_url)


class MailingListView(ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingDetailView(DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingUpdateForm
        if user.has_perm('mailing.can_stop_mailings'):
            return MailingManagerUpdateForm
        raise PermissionDenied


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    model = MailingSettings
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing/mailing_list')


class MailingLogListView(ListView):
    model = SendingAttempt
    template_name = 'mailing/mailing_log_list.html'
    context_object_name = 'object_list'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_detail')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save(commit=False)
            message.owner = self.request.user
            message.save()
            return redirect('mailing:message_detail', pk=message.pk)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'

    def get_queryset(self):
        return get_messages_from_cache()


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_detail')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.save()
            return redirect(self.success_url)


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_delete.html'
    success_url = reverse_lazy('mailing:index')
