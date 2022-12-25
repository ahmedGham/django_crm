import re
from tokenize import group
from cv2 import log
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import Group
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , allowed_users ,admin_only
# Create your views here.

@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "orders":orders,
        "customers":customers,
        "total_customers":total_customers,
        "total_orders": total_orders,
        "delivered":delivered,
        "pending": pending,
    }
    return render(request,"accounts/dashboard.html",context = context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        "products":products
        }
    return render(request, "accounts/products.html",context = context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.orders.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context={
        "orders":orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
    }
    return render(request,'accounts/user.html',context)


@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method =="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                messages.success(request,"Account wes created for "+ username)
                return redirect("login")
        context = {
             "form":form 
        }
        return render(request, "accounts/register.html",context=context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request,"username OR password is not correct") 

    return render(request,"accounts/login.html")



def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customers(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer__id=pk) # customer.orders.all() один хуй
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {
        "customer": customer,
        "orders": orders,
        "total_orders": total_orders,
        "myFilter":myFilter
    }
    return render(request, "accounts/customer.html",context = context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    if request.method =="POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/")

    elif request.method == "GET":
        context = {
            "form": OrderForm
        }
        return render(request,"accounts/order_form.html",context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)

        if form.is_valid():
            form.save()
        return redirect("/") 

    context = {
        "form": form
    }
    return render(request, "accounts/order_form.html", context)
        

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):

    selected_order = Order.objects.get(pk=pk)
    if request.method == "POST":
        selected_order.delete()
        return redirect("/")

    context = {
        "item":selected_order
    }    
    return render(request,"accounts/delete.html",context=context)        



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form':form
    }
    return render(request,'accounts/account_settings.html',context)