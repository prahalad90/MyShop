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
    # productCat = models.ForeignKey(Category, on_delete=models.CASCADE)
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

class Order(models.Model):
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
    totalPrice = models.FloatField(null=False)
    status = models.BooleanField(default=False)
    trackingcode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.id}/{self.trackingcode}"

    def track(self):
        return f"{self.id}/{self.trackingcode}"
    
    def grand_total(self,items):
        total = 0
        for i in items:
            price = i.product.price * i.quantity
            total+=price
        return total

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField()
    timeStamp = models.DateField()
    order = models.CharField(max_length=10, blank=True, null=True)
        
    def total(self):
        return self.product.price * self.quantity
    
    def grand_total(self, user):
        items = Cart.objects.filter(order=None, user=user)
        total = 0
        for i in items:
            price = i.product.price * i.quantity
            total+=price
        return total
    
    def image(self):
        return self.product.image

    def orderValue(self,id):
        items = Cart.objects.filter(order=id)
        total = 0
        for i in items:
            price = i.product.price * i.quantity
            total+=price
        return total