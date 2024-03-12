from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20)  

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCat = models.CharField(max_length=50)
    
    def __str__(self):
        return self.subCat

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    productSubCat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    product_name =  models.CharField(max_length=100)
    product_des = models.TextField()
    price = models.IntegerField()
    size = models.IntegerField(blank=True,null=True)
    color = models.CharField(max_length=20,blank=True, null=True)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images')
    
    def __str__(self):
        return self.product_name

class Shipping (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    F_name = models.CharField(max_length=50)
    L_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    trackingcode = models.CharField(max_length=50)
    isdeliverd = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.trackingcode}"


class Order(models.Model):
    order_no = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trackingcode = models.CharField(max_length=100,blank=True,null=True)
    orderValue = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    razorpay_payment_id = models.CharField(max_length = 150, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length = 150, blank=True, null=True)
    razorpay_signature = models.CharField(max_length = 150, blank=True, null=True)
    status = models.BooleanField(default=False)
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    timeStamp = models.DateField()
    trackingcode = models.CharField(max_length=10, blank=True, null=True)
    order_no = models.CharField(max_length=10, blank=True, null=True)
        
    def total(self):
        return self.product.price * self.quantity
    
    def grand_total(items):
        total = 0
        for i in items:
            price = i.product.price * i.quantity
            total+=price
        return total
    
    def image(self):
        return self.product.image

    def orderValue(id):
        items = Cart.objects.filter(trackingcode=id)
        total = 0
        for i in items:
            price = i.product.price * i.quantity
            total+=price
        return total