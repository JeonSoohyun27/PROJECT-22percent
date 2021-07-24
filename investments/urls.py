from django.urls import path

from investments.views import InvestmentHistoryView

urlpatterns = [
    path('/history', InvestmentHistoryView.as_view())
]