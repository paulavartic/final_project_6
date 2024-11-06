from django import forms
from mailing.models import MailingSettings, Client, Message
import datetime


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'clients':
                continue
            elif field_name == 'user':
                continue
            elif field_name == 'is_active':
                continue
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = MailingSettings
        fields = ['status', 'message', 'frequency']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)

    def clean_day(self):
        cleaned_data = self.cleaned_data['day']
        if 0 > cleaned_data > 31:
            raise forms.ValidationError('Invalid format')
        return cleaned_data


class MailingUpdateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        exclude = ['is_active']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['user'].disabled = True


class MailingManagerUpdateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        exclude = ['clients']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].disabled = True
        self.fields['body'].disabled = True
        self.fields['status'].disabled = True
        self.fields['first_send'].disabled = True
        self.fields['timestamp'].disabled = True
        self.fields['frequency'].disabled = True
        self.fields['user'].disabled = True


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']
        labels = {
            'full_name': 'Full name',
            'email': 'Email',
            'comment': 'Comment'
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
