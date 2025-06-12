from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from dds_manager.dds.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'


class ProductCreateView(CreateView):
    model = Transaction
    fields = '__all__'
    template_name = 'transaction_create.html'
    success_url = reverse_lazy('dds:base')


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'


class TransactionUpdateView(UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('dds:base')


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('dds:base')
