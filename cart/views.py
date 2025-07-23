from django.shortcuts import render , get_object_or_404
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(req):
    cart=Cart(req)
    cart_products=cart.get_products()
    quantities=cart.get_quantities()
    total_price=cart.get_total_price()
    return render(req,"cart_summary.html",{'cart_products':cart_products,'quantities':quantities,'total_price':total_price})


def cart_add(req):

    cart=Cart(req)
    if req.POST.get('action')=='post':
        product_id=int(req.POST.get('product_id'))
        product_qty=int(req.POST.get('product_qty'))
        product=get_object_or_404(Product,id=product_id)
        cart.add(product=product , quantity=product_qty)

        cart_quantity=cart.__len__()
        """ response=JsonResponse({'product name': product.name}) """
        response=JsonResponse({'cart_quantity': cart_quantity})
        messages.success(req,("Great choice! It's in your cart"))
        return response

def cart_delete(req):



    cart=Cart(req)
    if req.POST.get('action')=='post':
        product_id=int(req.POST.get('product_id'))
        
        
        cart.delete(product=product_id)
        response=JsonResponse({'productid': product_id})
        messages.success(req,("Successfully deleted."))
        return response






    
def cart_update(req):
   


    cart=Cart(req)
    if req.POST.get('action')=='post':
        product_id=int(req.POST.get('product_id'))
        product_qty=int(req.POST.get('product_qty'))
        
        cart.update(product=product_id,quantity=product_qty)
        response=JsonResponse({'cart_quantity': product_qty})
        messages.success(req,("Changes saved successfully."))
        return response
