from cart.models import Cart

def total_count(request):
    item_count=0
    u=request.user
    try:
        cart = Cart.objects.filter(user=u)
        for i in cart:
            item_count+=i.quantity
    except:
        item_count=0
    return {'item_count':item_count}