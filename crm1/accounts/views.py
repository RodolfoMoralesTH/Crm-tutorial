from django.db.models import fields
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import OrderForm
from django.forms import inlineformset_factory

from .models import *
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context={"orders":orders, "customers":customers, 'total_orders':total_orders, 'delivered':delivered,
    'pending':pending}

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer,'orders':orders,'order_count':order_count}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        #print('Printing POST:',request.POST)

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html',context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        #instance=order keeps the OrderForm from creating
        #a new object
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
