from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname=models.TextField(blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    city = models.TextField(blank=False, null=False)
    mobileno = models.CharField(max_length=15,blank=False, null=False)
    gender = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.username

class Table(models.Model):
    tableId = models.AutoField(primary_key=True)
    pax = models.IntegerField()
    price = models.IntegerField()

class BookTable(models.Model):
    cutomerId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # tableId = models.ForeignKey(Table, on_delete=models.CASCADE)
    fullname = models.TextField(blank=False, null=False)
    bookemail = models.TextField(blank=False, null=False)
    connum = models.TextField(blank=False, null=False)
    people = models.IntegerField(blank=False, null=False)
    bookdate = models.DateField(blank=False, null=False)
    booktime = models.TimeField(blank=False, null=False)
    booknote = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(blank=False, null=False)
    isCancelled = models.BooleanField(blank=False, null=False, default='False')
    finalPrice = models.FloatField()


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # type: ignore
    order_id = models.CharField(max_length=100)
    payer_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.payment_id} - {self.payment_status}'
    
    # admin
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=False, blank=False)

    def __str__(self):
        return self.name

