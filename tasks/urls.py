from django.urls import path
from .views import (
    TaskCreateView,
    TaskListView
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
]
