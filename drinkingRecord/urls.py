from django.urls import path
from .views import AlcoholRecordListCreateView, AlcoholRecordDetailView, MonthlyAlcoholConsumption, AlcoholAnalysisView

urlpatterns = [
    path('records/', AlcoholRecordListCreateView.as_view(), name='record-list-create'),
    path('records/<int:pk>/', AlcoholRecordDetailView.as_view(), name='record-detail'),
    path('calendar/', MonthlyAlcoholConsumption.as_view(), name='calendar'),
    path('analysis/', AlcoholAnalysisView.as_view(), name='alcohol-analysis'),
]
