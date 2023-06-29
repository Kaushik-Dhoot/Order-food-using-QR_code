from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class User(AbstractUser):

    email = None
    username = None
    phone = models.CharField(max_length=10, unique=True)
    phone_verified = models.BooleanField(default=False)
    cafe_manager = models.BooleanField(default=False)
    order_count = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


class menu_item(models.Model):

    item_id = models.AutoField
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='')
    desc = models.CharField(max_length=250)
    pic = models.ImageField(upload_to='fimage')
    price = models.CharField(max_length=4, default='0')
    list_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class rating(models.Model):

    name = models.CharField(max_length=30)
    comment = models.CharField(max_length=250)
    r_date = models.DateField()

    def __str__(self):
        return f"{self.name}\'s review"


class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=30, default='')
    phone = models.CharField(max_length=10, default='')
    table = models.CharField(max_length=15, default='take away')
    price = models.CharField(max_length=5, default='0')
    order_time = models.DateTimeField()
    bill_clear = models.BooleanField(default=False)


class bill(models.Model):
    order_items = models.CharField(max_length=5000)
    name = models.CharField(default='', max_length=50)
    bill_total = models.IntegerField()
    phone = models.CharField(max_length=10)
    bill_time = models.DateTimeField()
