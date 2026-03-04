from django.urls import path
from .views import OrdersView, ReportsView

urlpatterns = [
    path("mock/orders", OrdersView.as_view()),
    path("mock/reports", ReportsView.as_view()),
]