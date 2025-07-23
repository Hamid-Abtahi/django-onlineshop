from django.shortcuts import render , HttpResponse , redirect, get_object_or_404
from .models import Product , Category, Profile
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm , UpdateUserForm , UpdatePasswordForm, UpdateUserInfo
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm 
from payment.models import ShippingAddress, Order, OrderItem



def order_details(req, pk):
    if req.user.is_authenticated:
        order=Order.objects.get(id=pk)
        item=OrderItem.objects.filter(order=pk)
        context={
            'order':order,
            'item': item,
        }

    return render(req,'order_details.html', context)

def user_orders(req):
    if req.user.is_authenticated:
        delivered_orders=Order.objects.filter(user=req.user,status='Delivered')
        other_orders=Order.objects.filter(user=req.user).exclude(status='Delivered')
        context={
            'Delivered':delivered_orders,
            'Other':other_orders,

        }
        return render(req,'user_orders.html', context)


    else:
         messages.success(req,'Please log in first')
         return redirect('home')   
    



def search(req):

    if req.method=="POST":
        searched=req.POST['search']
        searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:

            messages.success(req,'No matching product found')
            return redirect('search')

        else:
            return render(req,'search.html',{'searched':searched})
        
    return render(req,'search.html')




def update_info(req):
    if req.user.is_authenticated:
        current_user=get_object_or_404(Profile, user__id=req.user.id)
        shipping_user=get_object_or_404(ShippingAddress,user__id=req.user.id)
        user_form=UpdateUserInfo(req.POST or None,instance = current_user)
        shipping_form=ShippingForm(req.POST or None,instance = shipping_user)
        
        if user_form.is_valid() or shipping_form.is_valid() :
            user_form.save()
            shipping_form.save()
            
            messages.success(req,'Great! Your user information was updated')
            return redirect('home')
        return render(req,'update_info.html',{'update_info': user_form, 'shipping_form': shipping_form})

    else:
        messages.success(req,'Please log in first')
        return redirect('home')
    

def category_summary(req):
    all_cats=Category.objects.all()
    return render(req,"category_summary.html",{'all_cats':all_cats})



def firstreq(Request):
    all_products= Product.objects.all()
    return render(Request,"index.html",{"products" : all_products})


def about(req):

    return render(req,"about.html")


def login_user(req):

    if req.method == "POST":

        username=req.POST["username"]
        password=req.POST["password"]
        user=authenticate(req , username=username , password=password)
        if user is not None:
            login(req,user)
            current_user=Profile.objects.get(user__id=req.user.id)
            save_cart=current_user.old_cart
            if save_cart:
                converted_cart=json.loads(save_cart)
                cart=Cart(req)
                for key, value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)

            messages.success(req,("Login successful"))
            return redirect("home")
        else:
            messages.success(req,("Login failed! Verify that your username and password are correct"))
            return redirect("login")
    else:

        return render(req,"login.html")

def logout_user(req):

    logout(req)
    messages.success(req,"Logout successful")
    return redirect("home")


def signup_user(req):
    form=SignUpForm()
    if req.method == "POST":
        form=SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data["username"]
            password1=form.cleaned_data["password1"]
            user=authenticate(req , username=username , password=password1)
            login(req,user)
            messages.success(req,("Your account has been created"))
            return redirect("update_info")
        else:
            
            messages.success(req,("Something went wrong during registration"))
            return render(req,"signup.html",{'form': form})
    else:

        return render(req,"signup.html",{'form':form})
    



def update_user(req):
    if req.user.is_authenticated:
        current_user=User.objects.get(id=req.user.id)
        user_form=UpdateUserForm(req.POST or None,instance = current_user)
        if user_form.is_valid():
            user_form.save()
            login(req,current_user)
            messages.success(req,'Great! Your profile was updated')
            return redirect('home')
        return render(req,'update_user.html',{'user_form': user_form})

    else:
        messages.success(req,'Please log in first')
        return redirect('home')





def update_password(req):

    if req.user.is_authenticated:
        current_user=req.user

        if req.method == "POST":
            form=UpdatePasswordForm(current_user,req.POST)

            if form.is_valid():
                form.save()
                messages.success(req,'Password changed successfully')
                login(req,current_user)
                return redirect('update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(req,error)
        
                return redirect('update_password')
        
        
        else:   
            form=UpdatePasswordForm(current_user)
            return render(req,'update_password.html',{'form':form})


    else:
        messages.success(req,'Please log in first')
        return redirect('home')
    






def product(Request,pk):
    product= Product.objects.get(id=pk)
    return render(Request,"product.html",{"products" : product})



def category(Request,cat):
    cat=cat.replace("-"," ")
    try:

        category=Category.objects.get(name=cat)
        products=Product.objects.filter(category=category)
        return render(Request,"category.html",{"products" : products,"category" : category})
    except:

        messages.success(Request,("Sorry, this category doesn't exist."))
        return redirect("home")