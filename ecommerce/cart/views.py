from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart,Account,Order

# Create your views here.
@login_required
def cartview(request):
    total=0
    u=request.user
    cart = Cart.objects.filter(user=u)
    for i in cart:
        total+=i.quantity * i.product.price
    return render(request, 'cartview.html', {'c': cart,'total':total})
@login_required
def addtocart(request,n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock-=1
            p.save()
    return redirect('cart:cartview')
@login_required
def removefromcart(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity -= 1
            cart.save()
            p.stock+=1
            p.save()
        else:
            cart.delete()
            p.stock+=1
            p.save()
    except:
        pass

    return redirect('cart:cartview')
@login_required
def deletecart(request,n):
    p = Product.objects.get(name=n)
    u = request.user
    cart = Cart.objects.get(user=u, product=p)
    try:
        cart.delete()
        p.stock += cart.quantity
        p.save()
        return redirect('cart:cartview')
    except:
        pass
@login_required
def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']

        u=request.user

        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total+=i.quantity * i.product.price
        try:
            ac=Account.objects.get(acctnum=n)
            if ac.amount >= total:
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=a,phone=p,order_status='Paid')
                    o.save()
                cart.delete()
                msg="Your Order Placed Successfully"
                return render(request, 'orderdetail.html', {'msg': msg})
            else:
                msg="Insufficient Fund. Your Order Not Placed"
                return render(request,'orderdetail.html',{'msg':msg})
        except:
            return HttpResponse('except')
    return render(request,'order_form.html')
@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o,})