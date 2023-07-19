import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganizerAndLoginRequiredMixin
from leads.models import Parties, Agent, Category
from .forms import (
    PartyModelForm, 
    AssignAgentForm, 
)


logger = logging.getLogger(__name__)


# CRUD+L - Create, Retrieve, Update and Delete + List

class PartyListView(LoginRequiredMixin, generic.ListView):
    template_name = "parties/party_list.html"
    context_object_name = "parties"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Parties.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Parties.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PartyListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Parties.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_parties": queryset
            })
        return context

class PartyDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "parties/party_detail.html"
    context_object_name = "party"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Parties.objects.filter(organization=user.userprofile)
        else:
            queryset = Parties.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class PartyCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "parties/party_create.html"
    form_class = PartyModelForm

    def get_success_url(self):
        return reverse("parties:party-list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['agent'].queryset = Agent.objects.filter(
            organization=user.userprofile
        )
        return form

    def form_valid(self, form):
        party = form.save(commit=False)
        party.organization = self.request.user.userprofile
        party.save()
        send_mail(
            subject="A party has been created",
            message="Go to the site to see the new party",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a party")
        return super(PartyCreateView, self).form_valid(form)


class PartyUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "parties/party_update.html"
    form_class = PartyModelForm
    context_object_name = "party"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        return Parties.objects.filter(organization=user.userprofile)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['agent'].queryset = Agent.objects.filter(
            organization=user.userprofile
        )
        return form

    def get_success_url(self):
        return reverse("parties:party-list")

    def form_valid(self, form):
        party_before_update = self.get_object()
        instance = form.save(commit=False)
        messages.info(self.request, "You have successfully updated this party")
        if party_before_update.last_updated_date != datetime.datetime.now():
                # this lead has now been converted
                instance.last_updated_date = datetime.datetime.now()
        instance.save()
        return super(PartyUpdateView, self).form_valid(form)



class PartyDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "parties/party_delete.html"

    def get_success_url(self):
        return reverse("parties:party-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of parties for the entire organization
        return Parties.objects.filter(organization=user.userprofile)
    

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "parties/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("parties:party-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        party = Parties.objects.get(id=self.kwargs["pk"])
        party.agent = agent
        party.save()
        return super(AssignAgentView, self).form_valid(form)

class PartyJsonView(generic.View):

    def get(self, request, *args, **kwargs):
        
        qs = list(Parties.objects.all().values(
            "first_name", 
            "last_name", 
            "primary_number",
            "whatsapp_number",
            "email",
            "preferred_contact_method",
            "organization")
        )

        return JsonResponse({
            "qs": qs,
        })