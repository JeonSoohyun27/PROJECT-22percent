from django.urls import path

from investments.views import InvestmentHistoryView, InvestmentPortfolioView 

urlpatterns = [
    path('/history'  , InvestmentHistoryView.as_view()),
    path('/portfolio', InvestmentPortfolioView.as_view()),
]
