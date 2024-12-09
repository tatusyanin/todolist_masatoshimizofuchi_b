
from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem, Category
from .forms import ToDoItemForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import TodoItem
from django.shortcuts import render
from .forms import ShoppingItemForm
from .models import ShoppingItem, Category
from .models import TodoItem, Store

import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # ログイン後にリダイレクトするURLを設定
    return render(request, 'login.html')

@login_required
def todo_list(request):
        categories = Category.objects.all()
        todos = TodoItem.objects.all()
        total_price = sum(todo.price or 0 for todo in todos) #値段の入力を任意
        context = {
        'categories': categories,
        'todos': todos,
    }
        if 'sort_by_price' in request.GET:#安い順に並べ替える
            todo_items = TodoItem.objects.order_by('price')
        else:
            todo_items = TodoItem.objects.order_by('store_id')

        context = {
        'todo_items': todo_items
    }
        return render(request, 'todo_list.html', context)

@login_required
def create_todo_item(request):
    if request.method == 'POST':
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.source = request.POST.get('source', 'default')
            todo_item.save()
            if todo_item.source == 'shopping':
                return redirect('shopping_todo')
            return redirect('todo_list')
    else:
        form = ToDoItemForm()
    categories = Category.objects.all()
    context = {
        'form': form,
        'stores': Store.objects.all()
    }
    return render(request, 'todo/create_todo_item.html', {'form': form, 'categories': categories})

@login_required
def mark_as_completed(request, todo_id):#完了ボタン
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    todo_item.completed = True
    todo_item.save()
    return redirect('todo_list')

def custom_logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def toggle_completed_status(request, todo_id):
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    todo_item.completed = not todo_item.completed
    todo_item.save()
    return redirect('todo_list')

@login_required
def todo_deleted(request):
    return render(request, 'todo/todo_deleted.html')

@login_required
def delete_todo_item(request, todo_id):
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    todo_item.delete()
    return redirect('todo_list')

@login_required
def edit_todo_item(request, todo_id):#編集
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    if request.method == 'POST':
        form = ToDoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()  # 編集された内容を保存
            if 'add_new' in request.POST:
                # 新しい ToDo アイテムを追加
                new_todo_item = form.save(commit=False)  # まだ保存せずにインスタンスを取得
                new_todo_item.id = None  # 新しい ID を割り当てる
                new_todo_item.save()  # 新しい ToDo アイテムを保存
                return redirect('todo_list')  # ToDo リストへリダイレクト
            return redirect('todo_list')  # 通常の保存後に ToDo リストへリダイレクト
    else:
        form = ToDoItemForm(instance=todo_item)
    return render(request, 'todo/edit_todo_item.html', {'form': form})


def newly_added_item_detail(request, todo_id):
    if request.method == 'POST':
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_todo_list')
    else:
        form = ToDoItemForm()
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    return render(request, 'todo/newly_added_item_detail.html', {'todo_item': todo_item})

@login_required
def delete_cheapest_items(request):#最安値を表示後削除
    items = TodoItem.objects.all()
    grouped_items = {}
    
    # 商品名ごとにアイテムをグループ化
    for item in items:
        if item.description not in grouped_items:
            grouped_items[item.description] = []
        grouped_items[item.description].append(item)
    
    # 最安値以外のアイテムを削除
    for description, items in grouped_items.items():
        items.sort(key=lambda x: x.price)  # 価格でソート
        for item in items[1:]:  # 最安値のアイテムを除く
            item.delete()
    
    return redirect('todo_list')

def logout_view(request):
    if request.method == 'GET':
        return redirect('logout_page')  # GET メソッドの場合、logout_page ビューにリダイレクト
    logout(request)
    return redirect('home')  # ログアウト後にリダイレクトするURLを設定
def logout_page(request):
    """
    ログアウトページのビュー
    """
    logout(request)
    return redirect('home')  # ログアウト後のリダイレクト先を指定



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):#サインアップ
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # サインアップ成功後にログインページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
from .models import ShoppingItem

def shopping_item_add(request):#買い物用
    if request.method == 'POST':
        form = ShoppingItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_todo')  # リダイレクト先のURLネームを確認
    else:
        form = ShoppingItemForm()
    return render(request, 'shopping_item_add.html', {'form': form})

def shopping_todo(request):
    items = ShoppingItem.objects.all()
    total_price = sum(item.prices * item.quantity for item in items if item.display_on_list)
    return render(request, 'shopping_todo.html', {'items': items, 'total_price': total_price})

def delete_shopping_item(request, item_id):#削除
    item = get_object_or_404(ShoppingItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('shopping_todo')
    return redirect('shopping_todo')

def calculate_total_price(request):#計算
    items = ShoppingItem.objects.all()
    total_price = sum(item.prices for item in items)
    return render(request, 'shopping_todo.html', {'items': items, 'total_price': total_price})

from django.shortcuts import redirect

def calculate_total(request):#合計額計算
    if request.method == 'POST':
        todos = TodoItem.objects.all()
        total_price = sum(todo.price for todo in todos)
        context = {
            'todos': todos,
            'total_price': total_price,
        }
        return render(request, 'todo_list.html', context)
    return redirect('todo_list')  # Todoリストページにリダイレクト