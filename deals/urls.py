from django.db.models.expressions import F
from django.urls import path

from deals.views import DealDetailView, DealsView, LoanAmountView, DealPaybackView

urlpatterns = [
    path(''                      , DealsView.as_view()),
    path('/<int:deal_id>'        , DealDetailView.as_view()),
    path('/loan-amount'          , LoanAmountView.as_view()),
    path('/<int:deal_id>/payback', DealPaybackView.as_view()),
]
