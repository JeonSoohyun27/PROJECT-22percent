from django.urls import path

from investments.views import InvestmentHistoryView, InvestDealView

urlpatterns = [
	path(''         , InvestDealView.as_view()),
    path('/history' , InvestmentHistoryView.as_view())
]
