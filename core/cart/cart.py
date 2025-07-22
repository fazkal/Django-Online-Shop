from shop.models import ProductModel,ProductStatusType
from cart.models import CartModel,CartItemModel

class CartSession:
    total_payment_price = 0
    def __init__(self,session):
        self.session = session
        self._cart = self.session.setdefault("cart",{"items":[]})
        #self.add_product()

    def update_product_quantity(self,product_id,quantity):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                item['quantity'] = int(quantity)
                break
        else:
            return
        self.save()

    def add_product(self,product_id):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                item['quantity']+=1
                break
        else:
            new_item = {
                'product_id': product_id,
                'quantity' : 1
            }
            self._cart['items'].append(new_item)
        self.save()

    def remove_product(self,product_id):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                self._cart['items'].remove(item)
                break
        else:
            return
        self.save()

    def clear(self):
        self._cart = self.session['cart'] = {"items":[]}
        self.save()

    def get_cart_dict(self):
        return self._cart
    
    def get_cart_items(self):
        cart_items = self._cart["items"]
        self.total_payment_price = 0
        for item in cart_items:
            product_obj = ProductModel.objects.get(id=item["product_id"],status=ProductStatusType.publish.value)
            item["product_obj"] = product_obj
            total_price = int(item["quantity"]) * product_obj.get_price()
            item["total_price"] = total_price
            self.total_payment_price += total_price
            item["stock_range"] = range(1, product_obj.stock + 1)
        return cart_items
    
    def get_total_payment_price(self):
        return self.total_payment_price

    def get_total_quantity(self):
        total_quantity = 0
        for item in self._cart['items']:
            total_quantity += item['quantity']
        return total_quantity

    def __len__(self):
        return len(self._cart['items'])

    def save(self):
        self.session.modified = True

    def sync_cart_items_from_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)

        for cart_item in cart_items:
            for item in self._cart['items']:
                if str(cart_item.product.id) == item['product_id']:
                    cart_item.quantity = item['quantity']
                    cart_item.save()
                    break
            else:
                new_item = {'product_id': str(cart_item.product.id),'quantity':cart_item.quantity}
                self._cart['items'].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()

    def merge_session_cart_in_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        
        for item in self._cart['items']:
            product_obj = ProductModel.objects.get(id=item["product_id"],status=ProductStatusType.publish.value)
            cart_item ,create = CartItemModel.objects.get_or_create(cart=cart,product=product_obj)
            cart_item.quantity = item['quantity']
            cart_item.save()
        session_product_ids = [item['product_id'] for item in self._cart['items']]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()