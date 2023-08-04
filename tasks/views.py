import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail, get_connection
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail.backends import console
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from agents.mixins import OrganizerAndLoginRequiredMixin
from .tokens import generate_token, verify_token
from leads.models import Task, Agent, UserProfile, TaskAttendees
from .forms import (
    TaskModelForm
)

print('task create view')
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

        #Sending "EMAILS"
        invited_user_ids = self.request.POST.getlist('invitees')
        invited_user_emails = []
        
        connection = get_connection(backend='django.core.mail.backends.console.EmailBackend')

        for id in invited_user_ids:
            invitee_user = UserProfile.objects.filter(user_id=id).first()
            accept_invite_link = self.request.build_absolute_uri(reverse("tasks:accept-invite", args=[task.id, generate_token(id)]))

            if invitee_user:
                invited_user_emails.append(invitee_user.user.email)
                
                for email in invited_user_emails:
                    #"EMAIL" content
                    subject = f"You're invited to work on {task.title}"
                    message = f"You have been invited to work on the task: '{task.title}'. Click on the link below to accept. {accept_invite_link}"
                    from_email = "lisa@gmail.com"
                    recipient_list = [email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False, connection=connection)

        messages.success(self.request, "You have successfully created a task and sent invites")
        return super(TaskCreateView, self).form_valid(form)
    
    def accept_invite(request, task_id, token):
        task = get_object_or_404(Task, pk=task_id)

        participant_id = verify_token(token)
        if participant_id is None:
            return HttpResponseBadRequest("Invalid token")
        
        participant_profile = UserProfile.objects.get(id=participant_id)
        TaskAttendees.objects.create(task=task, participant=participant_profile)
        return render(request, 'tasks/invitation_accepted.html', {'task': task})

class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Task.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Task.objects.filter(
                organization=user.agent.organization
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

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
