from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from shop.models import Product, Profile
from django.contrib.auth.models import User

def payment_success(req):

    return render(req,"payment/payment_success.html")


def checkout(req):
    
    cart=Cart(req)
    cart_products=cart.get_products()
    quantities=cart.get_quantities()
    total_price=cart.get_total_price()

    if req.user.is_authenticated:
        shipping_user=get_object_or_404(ShippingAddress,user__id=req.user.id)
        shipping_form=ShippingForm(req.POST or None, instance=shipping_user)

        return render(req,'payment/checkout.html',{'cart_products':cart_products,'quantities':quantities,
        'total_price':total_price,'shipping_form':shipping_form})
    
    else:
        shipping_form=ShippingForm(req.POST or None)
        return render(req,'payment/checkout.html',{'cart_products':cart_products,'quantities':quantities,
        'total_price':total_price,'shipping_form':shipping_form})



def confirm_order(req):
    if req.method == 'POST':
        cart=Cart(req)
        cart_products=cart.get_products()
        quantities=cart.get_quantities()
        total_price=cart.get_total_price()
        user_shipping=req.POST
        req.session['user_shipping']=user_shipping

        
        return render(req,'payment/confirm_order.html',{'cart_products':cart_products,'quantities':quantities,
            'total_price':total_price,'user_shipping':user_shipping})
        

    else:
        messages.success(req,'You do not have permission to access this page')
        return redirect('home')

    

def process_order(req):
    if req.POST:
        user_shipping=req.session.get('user_shipping')

        """ full_address=f"{user_shipping['shipping_address1']}\n{user_shipping['shipping_address2']}\n{user_shipping['shipping_city']}\n{user_shipping['state']}\n{user_shipping['shipping_zipcode']}\n{user_shipping['shipping_country']}" """
        
        cart=Cart(req)
        cart_products=cart.get_products()
        quantities=cart.get_quantities()
        total_price=cart.get_total_price()
        full_name=user_shipping['shipping_full_name']
        email=user_shipping['shipping_email']
        address_lines = [
            user_shipping.get("shipping_address1", ""),
            user_shipping.get("shipping_address2", ""),
            user_shipping.get("shipping_city", ""),
            user_shipping.get("state", ""),
            user_shipping.get("shipping_zipcode", ""),
            user_shipping.get("shipping_country", ""),
                        ]

        
        address_lines = [line for line in address_lines if line]

        full_address = "\n".join(address_lines)

        if req.user.is_authenticated:
            user=req.user
            new_order=Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total_price,

            )
            new_order.save()
            odr=get_object_or_404(Order, id=new_order.pk)
            for product in cart_products:
                prod=get_object_or_404(Product, id=product.id)
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                for k,v in quantities.items():
                    if int(k)==product.id:
                        new_item=OrderItem(
                            order=odr,
                            product=prod,
                            price=price,
                            quantity=v,
                            user=user,
                            
                        )

                        new_item.save()
            for key in list(req.session.keys()):
                if key=='session_key':
                    del req.session[key]
                    cu=Profile.objects.filter(user__id=req.user.id)
                    cu.update(old_cart="")
            messages.success(req,'Your order has been placed successfully')
            return redirect('home') 

        else:
            new_order=Order(
               
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total_price,
                
            )
            new_order.save() 

            for product in cart_products:
                prod=get_object_or_404(Product, id=product.id)
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                for k,v in quantities.items():
                    if int(k)==product.id:
                        new_item=OrderItem(
                            order=odr,
                            product=prod,
                            price=price,
                            quantity=v,
                            
                            
                        )

                    new_item.save()
            for key in list(req.session.keys()):
                if key=='session_key':
                    del req.session[key] 
            messages.success(req,'Your order has been placed successfully')
            return redirect('home') 

    else:
        messages.success(req,'You do not have permission to access this page')
        return redirect('home')

    