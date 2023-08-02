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
from leads.models import Task, Agent
from .forms import (
    TaskModelForm
)

class TaskCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "tasks/task_create.html"
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse("tasks:task-list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        # form.fields['agent'].queryset = Agent.objects.filter(
        #     organization=user.userprofile
        # )
        return form

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user.userprofile
        task.save()
        send_mail(
            subject="A task has been created",
            message="Go to the site to see the new task",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a task")
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.all()
            # filter for the agent that is logged in
            # queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Task.objects.all()
            # context.update({
            #     "unassigned_parties": queryset
            # })
        return context


def task_list(request):
    tasks = Task.objects.all()
    todo_tasks = tasks.filter(status='TODO')
    in_progress_tasks = tasks.filter(status='IN_PROGRESS')
    done_tasks = tasks.filter(status='DONE')
    print("here---------------------")
    return render(request, 'task_list.html', {'todo_tasks': todo_tasks, 'in_progress_tasks': in_progress_tasks, 'done_tasks': done_tasks})

