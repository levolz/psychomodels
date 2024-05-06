from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Psychmodel, Proposal, Framework


# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    cc_myself = forms.BooleanField(
        required=False, label="Send a copy to yourself", initial=True
    )

    def send_email(self, recipients: list = None):
        if self.is_valid() and recipients is not None:
            # name = self.cleaned_data["name"]
            sender = self.cleaned_data["email"]
            subject = self.cleaned_data["subject"]
            message = self.cleaned_data["message"]
            cc_myself = self.cleaned_data["cc_myself"]

            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)


class SubmitModelForm(forms.Form):
    class Meta:
        model = Proposal
        fields = [
            "title",
            "description",
            "publication",
        ]

    model_name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    publication = forms.CharField(required=False)

    def save(self, commit=True):
        model = Proposal()
        model.title = self.cleaned_data["model_name"]
        model.description = self.cleaned_data["description"]
        model.publication = self.cleaned_data["publication"]
        if commit:
            model.save()
        return model


class PsychmodelForm(forms.ModelForm):
    class Meta:
        model = Psychmodel
        fields = [
            "model_name",
            "description",
            # "publication",
            # "authors",
            "framework",
            "softwarepackage",
            "language",
        ]


class FrameworkForm(forms.ModelForm):
    class Meta:
        model = Framework
        fields = [
            "framework_name",
            "framework_description",
            "parent_framework",
            "publication",
            "explanation",
        ]
