
from django.urls import path
from .views import (
    KpiListView, KpiCreateView, TargetCreateView, TargetListView, load_cond2
)

app_name = "kpis"

urlpatterns = [
    path('', KpiListView.as_view(), name='kpi-list'),
    path('create-kpi', KpiCreateView.as_view(), name='kpi-create'),
    path('list-targets', TargetListView.as_view(), name='target-list'),
    path('create-target', TargetCreateView.as_view(), name='target-create'),

    path('ajax/load-cond2/', load_cond2, name='ajax_load_cond2')
]