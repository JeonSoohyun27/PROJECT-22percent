from django.urls import path

from investments.views import InvestmentHistoryView, InvestmentPortfolioView, InvestmentSummaryView, XlsxExportView

urlpatterns = [
    path('/history'  , InvestmentHistoryView.as_view()),
    path('/portfolio', InvestmentPortfolioView.as_view()),
    path('/summary'  , InvestmentSummaryView.as_view()),
    path('/export-investment-history-xlsx', XlsxExportView.as_view())
]
