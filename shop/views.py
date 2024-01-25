from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from .models import Product, Cart, Order
import datetime
from django.contrib import messages
from .forms import orderForm
from random import randint


# Create your views here.
def index(request):
    myCat = Product.objects.values('productSubCat')
    cats = {item['productSubCat'] for item in myCat}
    products = []
    for cat in cats:
        prod = Product.objects.filter(productSubCat = cat)
        products.append(prod)
    params = {'products':products}
    return render(request,'index.html',params)

def productview(request, id):
    product= Product.objects.get(pk=id)
    params ={'product':product}
    return render(request,'product.html',params)


def searchveiw(request):
    if request.method == 'GET':
        term = request.GET['term']    
        items = Product.objects.filter(product_name__contains = term)
        params = {
            'products':items,
            'term':term,
        }    
    return render(request,'search.html',params)

def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            product = request.GET.get('prdt')
            item = Product.objects.get(pk = product)
            cartItems = Cart.objects.filter(user = user, product = item,order=None)
            if cartItems:
                cartItems[0].quantity += 1
                cartItems[0].save()
            else:
                mycart= Cart.objects.create(user = user, product = item, quantity=1, timeStamp=datetime.date.today())
                mycart.save()
            return redirect(view_cart)
        else:
            return redirect(view_cart)
    return redirect(loginview)

def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        items = Cart.objects.all().filter(user=user, order= None)
        if items == None:
            return render(request, 'cart.html',{'msg':"No item in your cart"})
        else:
            total = Cart.grand_total(items,user)
            params = { 'cartitems':items,'total':total}
            return render(request, 'cart.html',params)
    return redirect(loginview)    

def remove_item(request,id):
    if request.user.is_authenticated:
        item = Cart.objects.get(pk=id)
        item.delete()
        return redirect(view_cart)

def less_qnt(request,id):
    qtn = Cart.objects.get(pk=id)
    if qtn.quantity > 1:
        qtn.quantity -= 1
        qtn.save()
        return redirect(view_cart)
    else:
        return redirect(view_cart)
    

def add_qnt(request,id):
    qtn = Cart.objects.get(pk=id)
    if qtn.quantity >= 5:
        messages.success(request, "Can't order more than 5 quantities")
        return redirect(view_cart)
    else:
        qtn.quantity += 1
        qtn.save()
        return redirect(view_cart)

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total = cart[0].grand_total()
        try:
            norder = Order.objects.get(user = user, status = False)
        except:
            norder = None
        if norder:
            return redirect ('placeorder') 
        else: 
            if request.method  == 'POST':
                fname = request.POST['FirstName']
                lname = request.POST['LastName']
                address1 = request.POST['address1']
                address2 = request.POST['address1']
                city = request.POST['city']
                state = request.POST['state']
                country = request.POST['country']
                pin = request.POST['pincode']
                email = request.POST['email']
                mobile = request.POST['mobile']
                trackingcode = randint(100000, 1000000)
                totalPrice = total
        
                order = Order(user = user ,F_name=fname,L_name=lname,address1=address1,address2=address2,city=city,state=state,country=country,pincode=pin,email=email,mobile=mobile,trackingcode=trackingcode,totalPrice=totalPrice)
                order.save()
                return redirect ('placeorder') 
    return render (request,'checkout.html')

def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.get(user=user, status=False)
        items = Cart.objects.filter(user = request.user, order = None)
        total = Cart.grand_total(items)
        params = {
            'order':order,
            'items': items,
            'total':total,
        }
        return render (request,'placeorder.html',params)

def orderconfirm(request, trackingcode):
    if request.user.is_authenticated:
        print(trackingcode)
        user = request.user
        order = Order.objects.get(trackingcode = trackingcode)
        
        code = order.track()
        cart = Cart.objects.filter(user = user, order=None)
        for i in cart:
            i.order = code
            i.save()
        params = {
            'order':order
        }
        order.status = True
        order.save()
        return render(request,'complete.html', params)
        
def order(request):
    if request.user.is_authenticated:
        user = request.user
        num = Cart.objects.values('order').exclude(order = None)
        ordernum = {item['order'] for item in num}
        orders = []
        for i in ordernum:
            order = Cart.objects.filter(order = i)
            orders.append(order)

        params = {
            'orders':orders
        }
        return render(request,'order.html', params)

def orderdetail(request,id):
    if request.user.is_authenticated:
        print(id)
        user = request.user
        item = Cart.objects.get(id=id)
        code  = item.order
        trackingcode  = code[2:]
        order = Order.objects.get(trackingcode=trackingcode)
        items = Cart.objects.filter(order = code)
        total = order.grand_total(items)
        params = {
            'order':order,
            'items': items,
            'total':total,
        }
        return render (request,'orderdetail.html',params)

def loginview(request):
    if request.method == "POST":
        id = request.POST['id']
        passw = request.POST['pass']
        user = authenticate(username=id, password=passw)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.success(request, "Invalid credential")
            return render(request,'login.html')
    return render(request,'login.html')


def logoutview(request):
    logout(request)
    return redirect(index)