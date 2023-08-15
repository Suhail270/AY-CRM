from django.urls import path
from . import views
from .views import (
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    OppTaskCreateView
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/create/', TaskCreateView.as_view(), name='task-create'),
    path('accept_invite/<int:task_id>/<str:token>/', TaskCreateView.accept_invite, name='accept-invite'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    # path('opportunity/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('opportunity/<int:pk>/create/', OppTaskCreateView.as_view(), name='opportunity-task-create'),
    # path('opportunity/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    # path('opportunity/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
