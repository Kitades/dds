from django.urls import path

from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    ReferenceManagementView,
    load_categories,
    load_subcategories, delete_reference
)

app_name = 'dds'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('edit/<int:pk>/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('references/', ReferenceManagementView.as_view(), name='manage_references'),
    path('load-categories/', load_categories, name='load_categories'),
    path('load-subcategories/', load_subcategories, name='load_subcategories'),
    path('references/delete/<str:ref_type>/<int:ref_id>/', delete_reference, name='delete_reference'),
]
