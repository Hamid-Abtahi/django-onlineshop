from shop.models import Product, Profile


class Cart:

    def __init__(self,req):
        self.session=req.session
        self.req=req

        cart=self.session.get('session_key')
        if 'session_key' not in req.session:
            cart=self.session['session_key']={}
        
        self.cart=cart



    def add(self,product,quantity):
        
        product_id=str(product.id)
        product_qty=str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)  
        
        self.session.modified=True

        if self.req.user.is_authenticated:
            current_user=Profile.objects.filter(user__id=self.req.user.id)
            db_cart=str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))

    
    def db_add(self,product,quantity):
        
        product_id=str(product)
        product_qty=str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)  
        
        self.session.modified=True

        if self.req.user.is_authenticated:
            current_user=Profile.objects.filter(user__id=self.req.user.id)
            db_cart=str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))





    def __len__(self):

        return len(self.cart)





    def get_products(self):

        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        return products


    def get_quantities(self):

        quantities=self.cart
        return quantities



    def get_total_price(self):

        product_ids=self.cart.keys()
        total_price=0

        products=Product.objects.filter(id__in=product_ids)
        for key,value in self.cart.items():

            key=int(key)

            for product in products:
                 
                 if product.id == key:

                    if product.is_sale:
                        total_price=total_price+(product.sale_price*value)

                    else:
                        total_price=total_price+(product.price*value)   

        return total_price
        


    def update(self,product,quantity):

        product_id=str(product)
        product_qty=int(quantity)

        ourcart=self.cart

        ourcart[product_id]=product_qty
        self.session.modified=True
        xx=self.cart
        if self.req.user.is_authenticated:
            current_user=Profile.objects.filter(user__id=self.req.user.id)
            db_cart=str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))
        return xx






    def delete(self,product):

        product_id=str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified=True

        if self.req.user.is_authenticated:
            current_user=Profile.objects.filter(user__id=self.req.user.id)
            db_cart=str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))