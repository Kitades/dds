from django.urls import path

from dds_manager.dds.apps import DdsConfig
from .views import TransactionListView, ProductCreateView, TransactionDetailView, TransactionUpdateView, TransactionDeleteView

app_name = DdsConfig.name

urlpatterns = [
    path('dds/', TransactionListView.as_view(), name='transaction_list'),
    path('dds/create/', ProductCreateView.as_view(), name='transaction_create'),
    path('dds/detail/int:<pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('dds/update/int:<pk>/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('dds/delete/int:<pk>/', TransactionDeleteView.as_view(), name='transaction_delete'),
]