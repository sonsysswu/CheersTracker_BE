from django.urls import path
from .views import AlcoholRecordListCreateView

urlpatterns = [
    path('records/', AlcoholRecordListCreateView.as_view(), name='record-list-create'),
]
