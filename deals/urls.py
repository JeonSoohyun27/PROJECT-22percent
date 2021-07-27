from django.urls import path

from deals.views import DealDetailView, DealsView, LoanAmountView

urlpatterns = [
    path('/<int:deal_id>', DealDetailView.as_view()),
    path('', DealsView.as_view()),
    path('/loan-amount', LoanAmountView.as_view())
]
