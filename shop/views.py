from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, logout, login
from .models import Product, Cart, Order, Shipping
import datetime
from django.contrib import messages
from random import randint
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    user = request.user
    myCat = Product.objects.values('productSubCat')
    cats = {item['productSubCat'] for item in myCat}
    products = []
    for cat in cats:
        prod = Product.objects.filter(productSubCat = cat)
        products.append(prod)
    
    items = Cart.objects.filter(user = user, order_no=None)
    params = {'products':products,'cartitems':items}
    return render(request,'index.html',params)

def productview(request, id):
    product= Product.objects.get(pk=id)
    items = Cart.objects.filter(user = request.user, order_no=None)
    params ={'product':product, 'cartitems':items}
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
            cartItems = Cart.objects.filter(user = user, product = item,order_no=None)
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
        items = Cart.objects.filter(user=user, order_no= None)
        if items == None:
            return render(request, 'cart.html',{'msg':"No item in your cart"})
        else:
            total = Cart.grand_total(items)
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
        items = Cart.objects.filter(user=user,order_no=None)
        total = Cart.grand_total(items)
        try:
            address = Shipping.objects.get(user = user, isdeliverd=False)
        except:
            address = None
        if address:
            return redirect ('placeorder') 
        else: 
            if request.method  == 'POST':
                fname = request.POST['FirstName']
                lname = request.POST['LastName']
                address1 = request.POST['address1']
                address2 = request.POST['address2']
                city = request.POST['city']
                state = request.POST['state']
                country = request.POST['country']
                pin = request.POST['pincode']
                email = request.POST['email']
                mobile = request.POST['mobile']
                trackingcode = randint(100000, 1000000)
                ShippingAddress = Shipping(user = user ,F_name=fname,L_name=lname,address1=address1,address2=address2,city=city,state=state,country=country,pincode=pin,email=email,mobile=mobile,trackingcode=trackingcode)
                ShippingAddress.save()
                return redirect ('placeorder') 
    return render (request,'checkout.html')


client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        shipping = Shipping.objects.get(user=user, isdeliverd=False)
        items = Cart.objects.filter(user = user, order_no = None)
        total = Cart.grand_total(items)

        try:
            order = Order.objects.get(user = user, status = False)
            payment = client.order.create({ "amount":total * 100, "currency": "INR", "receipt": order.trackingcode })
            order.orderValue=total
            order.razorpay_order_id =payment['id']
            order.save()
        except:
            order = Order(user=user,trackingcode=shipping.trackingcode,orderValue=total)
            order.save()
            payment = client.order.create({ "amount":total * 100, "currency": "INR", "receipt": order.trackingcode })
            order.razorpay_order_id =payment['id']  
            order.save()              
        callbackURL = 'http://127.0.0.1:8000/orderconfirm/'
        params = {
            'shipping':shipping,
            'items': items,
            'total':total,
            'payment':payment,
            'order_id':payment['id'],
            'orderId':order.trackingcode,
            'razorpay_merchant_id':settings.KEY,
            'callbackURL':callbackURL,
        }
        return render (request,'placeorder.html',params)
        
@csrf_exempt
def orderconfirm(request):
    user = request.user
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')
        order = Order.objects.get(razorpay_order_id = order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.status = True
        order.save()
        code = order.trackingcode
        shipping = Shipping.objects.get(trackingcode = code)
        shipping.isdeliverd = True
        shipping.save()
        items = Cart.objects.filter(user = user, order_no = None)
        for i in items:
            i.order_no = code
            i.save()
        
        return render(request, 'success.html')
    else:
        
        return render(request, 'success.html')
    
def order(request):
    if request.user.is_authenticated:
        user = request.user
        num = Cart.objects.values('order_no').exclude(order_no = None)
        ordernum = {item['order_no'] for item in num}
        orders = []
        for i in ordernum:
            order = Cart.objects.filter(order_no = i,user = user)
            orders.append(order)

        params = {
            'orders':orders
        }
        return render(request,'order.html', params)

def orderdetail(request,id):
    if request.user.is_authenticated:
        print(id)
        user = request.user
        address = Shipping.objects.get(trackingcode = id)
        items = Cart.objects.filter(order_no = id)
        total = Cart.orderValue(id)
        params = {
            'address':address,
            'items':items,
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

    