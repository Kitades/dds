from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Status, Type, Category, Subcategory, Transaction
from .forms import TransactionForm, ReferenceForm


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-date']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметры фильтрации из запроса
        filters = {
            'date_from': self.request.GET.get('date_from'),
            'date_to': self.request.GET.get('date_to'),
            'status': self.request.GET.get('status'),
            'type': self.request.GET.get('type'),
            'category': self.request.GET.get('category'),
            'subcategory': self.request.GET.get('subcategory'),
        }

        # Применяем фильтры
        if filters['date_from']:
            queryset = queryset.filter(date__gte=filters['date_from'])
        if filters['date_to']:
            queryset = queryset.filter(date__lte=filters['date_to'])
        if filters['status']:
            queryset = queryset.filter(status_id=filters['status'])
        if filters['type']:
            queryset = queryset.filter(type_id=filters['type'])
        if filters['category']:
            queryset = queryset.filter(category_id=filters['category'])
        if filters['subcategory']:
            queryset = queryset.filter(subcategory_id=filters['subcategory'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['filters'] = self.request.GET
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('dds:transaction_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создание транзакции'
        return context


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('dds:transaction_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактирование транзакции'
        return context


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('dds:transaction_list')
    context_object_name = 'transaction'




class ReferenceManagementView(TemplateView):
    template_name = 'reference_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReferenceForm()
        context['references'] = {
            'statuses': Status.objects.all(),
            'types': Type.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': Subcategory.objects.all(),
        }
        return context

    def post(self, request, *args, **kwargs):
        form = ReferenceForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            ref_type = form.cleaned_data['reference_type']
            name = form.cleaned_data['name']
            parent = form.cleaned_data.get('parent')

            if ref_type == ReferenceForm.STATUS:
                Status.objects.create(name=name)
            elif ref_type == ReferenceForm.TYPE:
                Type.objects.create(name=name)
            elif ref_type == ReferenceForm.CATEGORY:
                Category.objects.create(name=name, type=parent)
            elif ref_type == ReferenceForm.SUBCATEGORY:
                Subcategory.objects.create(name=name, category=parent)

            return redirect('manage_references')

        context['form'] = form
        return self.render_to_response(context)


def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id)
    return JsonResponse({
        'html': render_to_string('category_options.html', {'categories': categories})
    })


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse({
        'html': render_to_string('subcategory_options.html', {'subcategories': subcategories})
    })


def delete_reference(request, ref_type, ref_id):
    models_map = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory
    }

    model = models_map.get(ref_type)
    if not model:
        return redirect('manage_references')

    item = get_object_or_404(model, pk=ref_id)
    item.delete()

    return redirect('manage_references')
