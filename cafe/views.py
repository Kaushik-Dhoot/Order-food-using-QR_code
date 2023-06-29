from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib import messages
from cafe.models import *
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime, timedelta
import json, ast
from itertools import groupby
from django.db.models import Sum

User = get_user_model()


def menu(request):
    context = {}

    menu_items = menu_item.objects.all().order_by('list_order')
    items_by_category = {}

    for key, group in groupby(menu_items, key=lambda x: x.category):
        items_by_category[key] = list(group)

    context = {'items_by_category': items_by_category}

    return render(request, 'menu.html', context)


def all_orders(request):

    context = {}
    orders = order.objects.all().order_by('-order_time')
    order_by_table = {}

    for key, group in groupby(orders, key=lambda x: x.table):
        order_by_table[key] = list(group)

    for table, orders in order_by_table.items():
        for ord in orders:
            items_json_str = ord.items_json
            ord.items_json = json.loads(items_json_str)

    context = {'order_by_table': order_by_table}

    return render(request, 'all_orders.html', context)


def offers(request):
    return render(request, 'offers.html')


def reviews(request):

    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        cmt = request.POST.get('comment')
        date_today = date.today()

        review = rating(name=fname + ' ' + lname,
                        comment=cmt,
                        r_date=date_today)
        review.save()

    all_reviews = rating.objects.all().order_by('-r_date')
    context = {}
    context['reviews'] = all_reviews

    return render(request, 'reviews.html', context)


def profile(request):
    if request.user.is_anonymous:
        messages.error(request, 'Please Login first!!')
        return redirect('login')
    return render(request, 'profile.html')


def manage_menu(request):
    if request.method == 'POST' and request.FILES['img']:
        if (request.user.is_anonymous):
            messages.error(request, 'Please Login to continue!')
            return redirect('login')
        if not ((request.user.is_superuser) or (request.user.cafe_manager)):
            messages.error(request, 'Only Staff members are allowed!')
            return redirect('menu')
        else:
            name = request.POST.get('name')
            price = request.POST.get('price')
            desc = request.POST.get('desc')
            cat = request.POST.get('cat')
            img = request.FILES['img']

            if cat.lower() == 'papad':
                lising_order = 1
            elif cat.lower() == 'starter':
                listing_order = 2
            elif cat.lower() == 'bread':
                listing_order = 4
            elif cat.lower() == 'gravy':
                listing_order = 3
            elif cat.lower() == 'dal':
                listing_order = 5
            elif cat.lower() == 'rice':
                listing_order = 6
            elif cat.lower() == 'dessert':
                listing_order = 7
            elif cat.lower() == 'beverage':
                listing_order = 8

            dish = menu_item(name=name,
                             price=price,
                             desc=desc,
                             category=cat.lower(),
                             pic=img,
                             list_order=listing_order)
            dish.save()
            messages.success(request, 'Dish added successfully!')
            return redirect('menu')

    return render(
        request,
        'manage_menu.html',
    )


def delete_dish(request, item_id):

    dish = get_object_or_404(menu_item, id=item_id)
    if request.user.is_superuser:
        if request.method == 'POST':
            dish.delete()
            messages.success(request, 'Dish removed successfully!')
            return redirect('menu')
    else:
        messages.error(request, 'Only admins are allowed!')
        return redirect('menu')


def cart(request):

    if request.method == 'POST':
        if request.user.is_anonymous:
            name = 'Unknown'
            phone = 'Unknown'
        else:
            name = request.user.first_name + ' ' + request.user.last_name
            phone = request.user.phone
        items_json = request.POST.get('items_json')
        table_number = request.POST.get('table_value')
        total = request.POST.get('price')
        print(total)

        now = datetime.now()
        now_ist = now + timedelta(hours=5, minutes=30)

        if table_number == 'null':
            table_number = 'Take Away'

        new_order = order(name=name,
                          phone=phone,
                          items_json=items_json,
                          table=table_number,
                          order_time=now_ist,
                          price=total)
        new_order.save()

        if request.user.is_anonymous:
            messages.success(
                request,
                'Order Placed!! Thanks for ordering. You can sign up to save your information!!'
            )
            return redirect('/')
        else:

            usr = User.objects.get(phone=phone)
            usr.order_count += 1
            usr.save()
            messages.success(request, 'Order Placed!! Thanks for ordering')
            return redirect('my_orders')

    return render(request, 'cart.html')


def my_orders(request):

    phone = request.user.phone

    context = {}
    orders = order.objects.filter(phone=phone)
    order_by_table = {}

    for key, group in groupby(orders, key=lambda x: x.table):
        order_by_table[key] = list(group)
    for table, orders in order_by_table.items():
        for ord in orders:
            items_json_str = ord.items_json
            ord.items_json = json.loads(items_json_str)

    context = {'order_by_table': order_by_table}

    return render(request, 'my_orders.html', context)


def Login(request):

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(phone=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully !')
            return redirect('profile')

        else:
            messages.error(request, 'Login failed, Invalid Credentials!')
            return redirect('login')

    return render(request, 'login.html')


def Logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully !')
    return redirect('login')


def signup(request):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('number')
        pass_word = request.POST.get('password')
        c_pass_word = request.POST.get('cpassword')

        if User.objects.filter(phone=phone).exists():
            messages.error(
                request,
                'Mobile number already regestired. Please Login to continue')
            return redirect('login')

        my_user = User.objects.create_user(phone=phone, password=pass_word)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        messages.success(request, 'User created successfully !!')

        return redirect('login')

    return render(request, 'signup.html')


def generate_bill(request):
    t_number = request.GET.get('table')

    order_for_table = order.objects.filter(table=t_number, bill_clear=False)
    total_bill = 0
    now = datetime.now()
    now_ist = now + timedelta(hours=5, minutes=30)

    bill_items = []
    c_name = ''
    c_phone = ''
    for o in order_for_table:
        total_bill += int(o.price)
        o.bill_clear = True
        o.save()

        bill_items.append({
            'order_items': o.items_json,
        })
        c_name = o.name
        c_phone = o.phone

    order_dict = {}
    for item in bill_items:
        for key, value in item.items():
            order_items = json.loads(value)
            for pr_key, pr_value in order_items.items():
                order_dict[pr_value[1].lower()] = [
                    pr_value[0], (pr_value[2] * pr_value[0])
                ]
    new_bill = bill(order_items=order_dict,
                    name=c_name,
                    bill_total=total_bill,
                    phone=c_phone,
                    bill_time=now_ist)
    new_bill.save()

    context = {}

    context = {
        'order_dict': order_dict,
        'bill_total': total_bill,
        'name': c_name,
        'phone': c_phone,
        'inv_id': new_bill.id,
    }
    return render(request, 'generate_bill.html', context)


def view_bills(request):

    if request.user.is_anonymous:
        messages.error(request, 'You Must be an admin user to view this!')
        return redirect('')

    all_bills = bill.objects.all().order_by('-bill_time')

    for b in all_bills:
        b.order_items = ast.literal_eval(b.order_items)

    context = {'bills': all_bills}

    return render(request, 'bills.html', context)
