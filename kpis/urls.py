
from django.urls import path
from .views import (
    KpiListView, KpiCreateView, KpiUpdateView, TargetCreateView, TargetListView, TargetUpdateView, KpiUpdateViewNew, load_cond2, load_cond1, load_cond_op, load_list_contents, load_targets, load_agents
)

app_name = "kpis"

urlpatterns = [
    path('', KpiListView.as_view(), name='kpi-list'),
    path('create-kpi', KpiCreateView.as_view(), name='kpi-create'),
    # path('<int:pk>/update', KpiUpdateView.as_view(), name='kpi-update'),
    path('<int:pk>/update', KpiUpdateViewNew.as_view(), name='kpi-update'),
    path('list-targets', TargetListView.as_view(), name='target-list'),
    path('create-target', TargetCreateView.as_view(), name='target-create'),
    path('target/<int:pk>/update/', TargetUpdateView.as_view(), name='target-update'),

    path('ajax/load-cond2/', load_cond2, name='ajax_load_cond2'),
    path('ajax/load-cond1/', load_cond1, name='ajax_load_cond1'),
    path('ajax/load-agents/', load_agents, name='ajax_load_agents'),
    path('ajax/load-cond-op/', load_cond_op, name='ajax_load_cond_op'),
    path('ajax/load-list-contents/', load_list_contents, name='ajax_load_list_contents'),
    path('ajax/load-targets/', load_targets, name='ajax_load_targets')
]