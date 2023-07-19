from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from leads.models import Lead, Agent, Category, FollowUp, Parties

User = get_user_model()


class PartyModelForm(forms.ModelForm):
    class Meta:
        model = Parties
        fields = (
            'first_name',
            'last_name',
            'user_type',
            'primary_number',
            'whatsapp_number',
            'email',
            'preferred_contact_method',
            'agent'
        )

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        # if data != "Joe":
        #     raise ValidationError("Your name is not Joe")
        return data

    def clean(self):
        pass
        # first_name = self.cleaned_data["first_name"]
        # last_name = self.cleaned_data["last_name"]
        # if first_name + last_name != "Joe Soap":
        #     raise ValidationError("Your name is not Joe Soap")



class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents
