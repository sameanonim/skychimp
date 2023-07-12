from django.urls import path
from blog.apps import BlogConfig
from blog.views import RecordListView, RecordDetailView, RecordCreateView, RecordUpdateView, RecordDeleteView, \
    toggle_activity

app_name = BlogConfig.name

urlpatterns = [
    path('records/', RecordListView.as_view(), name='record_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('records_create/', RecordCreateView.as_view(), name='create_record'),
    path('records_update/<slug:slug>/', RecordUpdateView.as_view(), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
    path('toggle/<slug:slug>/', toggle_activity, name='toggle_activity')
]
