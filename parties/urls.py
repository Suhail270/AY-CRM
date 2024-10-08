from django.urls import path
from .views import (
    PartyListView, PartyDetailView, PartyCreateView, PartyUpdateView, PartyDeleteView,
    AssignAgentView, PartyJsonView
)

app_name = "parties"

urlpatterns = [
    path('', PartyListView.as_view(), name='party-list'),
    path('json/', PartyJsonView.as_view(), name='party-list-json'),
    path('<int:pk>/', PartyDetailView.as_view(), name='party-detail'),
    path('<int:pk>/update/', PartyUpdateView.as_view(), name='party-update'),
    path('<int:pk>/delete/', PartyDeleteView.as_view(), name='party-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('create/', PartyCreateView.as_view(), name='party-create'),
]