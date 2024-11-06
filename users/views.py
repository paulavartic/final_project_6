from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from config import settings
from users.forms import UserCreateForm, UserProfileForm, UserManagerForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:verification')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Email confirmation',
                message=f'Your code is {new_user.ver_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/verification.html'

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        user_code = User.objects.filter(verification_code=verification_code).first()

        if user_code is not None and user_code.verification_code == verification_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verification_error')


class ErrorVerification(TemplateView):
    template_name = 'users/verification_error.html'
    success_url = reverse_lazy('users:verification')


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user


class UserManagerProfileView(UpdateView):
    model = User
    form_class = UserManagerForm
    template_name = 'users/profile_manager.html'
    success_url = reverse_lazy('users:users_list')


class UserManagerListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'objects_list'
