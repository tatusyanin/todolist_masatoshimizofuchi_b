from django import forms
from .models import TodoItem, Category
from .models import TodoItem, Store
from .models import ShoppingItem
from .models import ShoppingItem, Category
from .models import ShoppingItem,Store

class ToDoItemForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日']
    )

    PRIORITY_CHOICES = [
        ('低', '低'),
        ('中', '中'),
        ('高', '高'),
        ('まじ高い', 'まじ高め'),
        ('最速でやれよ','最速でやれよ')
    ]
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="選択してください",
        to_field_name='name'
    )
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        empty_label="選択してください",
    )

    class Meta:
        model = TodoItem
        fields = ['description', 'due_date', 'priority', 'price', 'category', 'store', 'is_shopping']
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=True, empty_label="選択してください")


class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ['item_name','prices','category','quantity']  # 必要に応じてフィールドを追加
        widgets = {
            'category': forms.Select()
        }
