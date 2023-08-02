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
from leads.models import Task, Agent, UserProfile
from .forms import (
    TaskModelForm
)

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "tasks/task_create.html"
    form_class = TaskModelForm
    
    def get_success_url(self):
        return reverse("tasks:task-list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        # form.fields['status'].queryset = Category.objects.filter(
        #     organization=user.userprofile
        # )
        # form.fields['agent'].queryset = Agent.objects.filter(
        #     organization=user.userprofile
        # )
        # form.fields['party'].queryset = Parties.objects.filter(
        #     organization=user.userprofile
        # )
        if user.is_agent:
            org = Agent.objects.get(user = self.request.user).organization
        elif user.is_organizer:
            org = UserProfile.objects.get(user = self.request.user)
        form.fields['designated_lead'].queryset = UserProfile.objects.filter()
        # form.fields['invitees'].queryset = UserProfile
        return form

    def form_valid(self, form):
        task = form.save(commit=False)
        if self.request.user.is_organizer:
            task.organization = self.request.user.userprofile
        else:
            task.organization = Agent.objects.get(user = self.request.user).organization
        task.owner = self.request.user.userprofile
        task.save()
        # send_mail(
        #     subject="A lead has been created",
        #     message="Go to the site to see the new lead",
        #     from_email="test@test.com",
        #     recipient_list=["test2@test.com"]
        # )
        messages.success(self.request, "You have successfully created a task")
        return super(TaskCreateView, self).form_valid(form)

class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        # if user.is_organizer:
        #     queryset = Task.objects.filter(
        #         organization=user.userprofile
        #     )
        # else:
        #     queryset = Task.objects.filter(
        #         organization=user.agent.organization
        #     )
        #     # filter for the agent that is logged in
        #     queryset = queryset.filter(agent__user=user)
        # return queryset
        return Task.objects

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        # if user.is_organizer:
        #     queryset = Task.objects.filter(
        #         organization=user.userprofile, 
        #         agent__isnull=True
        #     )
        #     context.update({
        #         "unassigned_leads": queryset
        #     })
        return context
