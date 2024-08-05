from django.urls import path
from .views import AlcoholRecordListCreateView, AlcoholRecordDetailView, MonthlyAlcoholConsumption, AlcoholAnalysisView

urlpatterns = [
    path('records/', AlcoholRecordListCreateView.as_view(), name='record-list-create'),
    path('records/<str:date_str>/', AlcoholRecordDetailView.as_view(), name='record-detail'),  # 날짜 기반 조회
    path('calendar/', MonthlyAlcoholConsumption.as_view(), name='calendar'),
    path('analysis/', AlcoholAnalysisView.as_view(), name='alcohol-analysis'),
]
