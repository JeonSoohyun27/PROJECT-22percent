from django.urls import path

from deals.views import DealDetailView, DealsView

urlpatterns = [
    path('/<int:deal_id>', DealDetailView.as_view()),
    path('', DealsView.as_view())
]
