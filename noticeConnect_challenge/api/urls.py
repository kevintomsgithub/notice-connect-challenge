from django.urls import path
from .views import api_overview, \
    RecordAPIViews, RecordDetailsViews, \
    NoticeAPIViews, NoticeDetailsViews, \
    MatchAPIViews

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('notices/', NoticeAPIViews.as_view(), name='list-all-notices'),
    path('records/', RecordAPIViews.as_view(), name='list-all-records'),
    path('matches/', MatchAPIViews.as_view(), name='list-all-matches'),
    path('notices/<int:id>', NoticeDetailsViews.as_view(), name='get-notice-details'),
    path('records/<int:id>', RecordDetailsViews.as_view(), name='get-record-details'),
]