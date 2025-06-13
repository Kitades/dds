from django import forms
from .models import *


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        transaction_type = cleaned_data.get('type')

        if category and transaction_type and category.type != transaction_type:
            raise forms.ValidationError(
                "Выбранная категория не принадлежит выбранному типу"
            )

        if subcategory and category and subcategory.category != category:
            raise forms.ValidationError(
                "Выбранная подкатегория не принадлежит выбранной категории"
            )

        return cleaned_data


class ReferenceForm(forms.Form):
    STATUS = 'status'
    TYPE = 'type'
    CATEGORY = 'category'
    SUBCATEGORY = 'subcategory'

    REFERENCE_TYPES = (
        (STATUS, 'Статусы'),
        (TYPE, 'Типы'),
        (CATEGORY, 'Категории'),
        (SUBCATEGORY, 'Подкатегории'),
    )

    reference_type = forms.ChoiceField(choices=REFERENCE_TYPES)
    name = forms.CharField(max_length=100)
    parent = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        ref_type = cleaned_data.get('reference_type')
        parent = cleaned_data.get('parent')

        if ref_type == self.SUBCATEGORY and not parent:
            raise forms.ValidationError(
                "Для подкатегории необходимо выбрать категорию"
            )

        if ref_type == self.CATEGORY and not parent:
            raise forms.ValidationError(
                "Для категории необходимо выбрать тип"
            )

        return cleaned_data
