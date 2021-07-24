from django.urls import path
from deals.views import DealDetailView

urlpatterns = [
    path('/<int:deal_id>', DealDetailView.as_view()),
]