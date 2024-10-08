
from django.urls import path
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView,
    AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, LeadJsonView, 
    FollowUpCreateView, FollowUpUpdateView, FollowUpDeleteView, OpportunityListView, OpportunityConvertView,
    OpportunityUpdateView,OpportunityDetailView,OppFollowUpCreateView,OppFollowUpUpdateView,TimelineView,OppTimelineView
)

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('json/', LeadJsonView.as_view(), name='lead-list-json'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='lead-followup-create'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='lead-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('opportunities/', OpportunityListView.as_view(), name='opportunity-list'),
    path('<int:pk>/opportunities/convert/', OpportunityConvertView.as_view(), name='opportunity-convert'),
    path('opportunities/<int:pk>/update/', OpportunityUpdateView.as_view(), name='opportunity-update'),
    path('opportunities/<int:pk>/', OpportunityDetailView.as_view(), name='opportunity-detail'),
    path('opportunities/<int:pk>/followups/create/', OppFollowUpCreateView.as_view(), name='opportunity-followup-create'),
    path('opportunities/followups/<int:pk>/', OppFollowUpUpdateView.as_view(), name='opportunity-followup-update'),
    path('<int:pk>/timeline', TimelineView.as_view(), name='timeline'),
    path('opportunities/<int:pk>/timeline', OppTimelineView.as_view(), name='opportunity-timeline'),



]