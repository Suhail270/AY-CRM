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
from leads.models import Task, Agent, UserProfile,TaskStatusOptions,Lead,RepeatOptions
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
        # form.fields['agent'].queryset = Agent.objects.filter(
        #     organization=user.userprofile
        # )
        # form.fields['party'].queryset = Parties.objects.filter(
        #     organization=user.userprofile
        # )
        if user.is_agent:
            org = Agent.objects.get(user = self.request.user).organization
            form.fields['designated_agent'].queryset = UserProfile.objects.filter(user = user)
            form.fields['invitees'].queryset = UserProfile.objects.filter(user = user)
        elif user.is_organizer:
            org = UserProfile.objects.get(user = self.request.user)
            form.fields['designated_agent'].queryset = UserProfile.objects.filter()
        # form.fields['lead'].queryset = Lead.objects.filter(organization=user.userprofile)
        
        # form.fields['invitees'].queryset = UserProfile
        return form

    def form_valid(self, form):
        task = form.save(commit=False)
        user = self.request.user
        if user.is_organizer:
            task.owner = self.request.user.userprofile
        elif user.is_agent:
            task.owner = self.request.user.agent.organization
            task.designated_agent = self.request.user.userprofile

        try: 
            task.organization = self.request.user.agent.organization
        except: 
            pass
        try:
            task.status = TaskStatusOptions.objects.get(option = "TODO")
        except Exception as e: 
            print(e)
            pass
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
            queryset = Task.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Task.objects.filter(
                organization=user.agent.organization
            )
            
            # filter for the agent that is logged in
            queryset = queryset.filter(designated_agent=user.userprofile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            try: 
                querysetTODO = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "TODO"))
                querysetIN_PROGRESS = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "IN_PROGRESS"))
                querysetDONE = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "DONE"))
                
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })
            except: 
                querysetTODO = Task.objects.all()
                querysetIN_PROGRESS = Task.objects.all()
                querysetDONE = Task.objects.all()
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })

        else:
            queryset = Task.objects.filter(
                designated_agent=user.userprofile
            )
            
            try: 
                querysetTODO = queryset.filter(status = TaskStatusOptions.objects.get(option = "TODO"))
                querysetIN_PROGRESS = queryset.filter(status = TaskStatusOptions.objects.get(option = "IN_PROGRESS"))
                querysetDONE = queryset.filter(status = TaskStatusOptions.objects.get(option = "DONE"))
                
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })
            except: 
                querysetTODO = queryset.all()
                querysetIN_PROGRESS = queryset.all()
                querysetDONE = queryset.all()
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })

            
    
        return context


def task_list(request):
    tasks = Task.objects.all()
    todo_tasks = tasks.filter(status='TODO')
    in_progress_tasks = tasks.filter(status='IN_PROGRESS')
    done_tasks = tasks.filter(status='DONE')
    print("here---------------------")
    return render(request, 'task_list.html', {'todo_tasks': todo_tasks, 'in_progress_tasks': in_progress_tasks, 'done_tasks': done_tasks})

class  TaskNotificationView(LoginRequiredMixin, generic.ListView):
    template_name = "tasks/task_notification.html"
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
            queryset = queryset.filter(designated_agent=user.userprofile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskNotificationView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            try: 
                querysetTODO = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "TODO"))
                querysetIN_PROGRESS = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "IN_PROGRESS"))
                querysetDONE = Task.objects.filter(status = TaskStatusOptions.objects.get(option = "DONE"))
                
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })
            except: 
                querysetTODO = Task.objects.all()
                querysetIN_PROGRESS = Task.objects.all()
                querysetDONE = Task.objects.all()
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })

        else:
            queryset = Task.objects.filter(
                designated_agent=user.userprofile
            )
            
            try: 
                querysetTODO = queryset.filter(status = TaskStatusOptions.objects.get(option = "TODO"))
                querysetIN_PROGRESS = queryset.filter(status = TaskStatusOptions.objects.get(option = "IN_PROGRESS"))
                querysetDONE = queryset.filter(status = TaskStatusOptions.objects.get(option = "DONE"))
                
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })
            except: 
                querysetTODO = queryset.all()
                querysetIN_PROGRESS = queryset.all()
                querysetDONE = queryset.all()
                context.update({
                    "task_todo": querysetTODO,
                    "task_in_progress":querysetIN_PROGRESS,
                    "task_done":querysetDONE
                })

            
    
        return context


def task_list(request):
    tasks = Task.objects.all()
    todo_tasks = tasks.filter(status='TODO')
    in_progress_tasks = tasks.filter(status='IN_PROGRESS')
    done_tasks = tasks.filter(status='DONE')
    print("here---------------------")
    return render(request, 'task_list.html', {'todo_tasks': todo_tasks, 'in_progress_tasks': in_progress_tasks, 'done_tasks': done_tasks})




class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tasks/task_detail.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.all()
            queryset = queryset.filter(designated_agent=UserProfile.objects.get(user = user))

            # filter for the agent that is logged in
            # queryset = queryset.filter(agent__user=user)
        return queryset
    
class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tasks/task_update.html"
    form_class = TaskModelForm
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        queryset = Task.objects.all()
        if user.is_agent:
            queryset = queryset.filter(designated_agent=UserProfile.objects.get(user = user))
        return queryset
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['lead'].querysey = Lead.objects.filter(
            organization=user.userprofile
        )
        form.fields['designated_agent'].queryset = UserProfile.objects.filter(
            # organization=user.userprofile
        )
        form.fields['status'].queryset = TaskStatusOptions.objects.all()
        form.fields['repeat'].queryset = RepeatOptions.objects.all()
        return form

    def get_success_url(self):
        return reverse("tasks:task-list")

    def form_valid(self, form):
        updatedTask = self.get_object()
        instance = form.save(commit=False)
        messages.info(self.request, "You have successfully updated this task")
        if instance.status == TaskStatusOptions.objects.get(option = "DONE"):
                # this task has now been completed
                if(instance.end_date == None):
                    instance.end_date = datetime.datetime.now()
        instance.save()
        return super(TaskUpdateView, self).form_valid(form)

class TaskDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "tasks/task_delete.html"

    def get_success_url(self):
        return reverse("tasks:task-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of parties for the entire organization
        return Task.objects.all()
    