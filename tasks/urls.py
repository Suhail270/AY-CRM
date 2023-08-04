from django.urls import path
from . import views
from .views import (
    TaskCreateView,
    TaskListView
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('accept_invite/<int:task_id>/<str:token>/', TaskCreateView.accept_invite, name='accept-invite'),
]
