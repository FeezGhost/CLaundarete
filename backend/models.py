from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="default-profile.png")
    address = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)

class Launderer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="default-profile.png")
    address = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.username)

class Launderette(models.Model):
    launderer = models.ForeignKey(Launderer, null=True, on_delete= models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    available_time = models.CharField(max_length=500, null=True, blank=True)
    cover_photo = models.ImageField(null=True, blank=True, default="0_GettyImages-1068728612.jpg")
    location = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)

class Services(models.Model):
    launderette = models.ForeignKey(Launderette, null=True, on_delete= models.SET_NULL)
    title = models.CharField(max_length=200, null=True, unique=True)
    price = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.title)


class StatusChoice1(models.TextChoices):
    PENDING = 'pending', 'Pending'
    FINISHED = 'finished', 'Finished'
    ONGOING = 'ongoing', 'Ongoing'
    DECLINED = 'declined', 'Declined'


class Order(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
    launderette = models.ForeignKey(Launderette, null=True, on_delete= models.SET_NULL)
    description = models.CharField(max_length=200, null=True)
    price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    status =models.CharField(max_length=50, blank=True, null=True,choices=StatusChoice1.choices,default=StatusChoice1.PENDING)
    date_started = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_end = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.client.name)


class StatusChoice2(models.TextChoices):
    PENDING = 'pending', 'Pending'
    DELIVERED = 'delivered', 'Delivered'
    SENT = 'sent', 'Sent'


class Delivery(models.Model):
    client = models.OneToOneField(Client, null=True, on_delete= models.SET_NULL)
    launderette = models.OneToOneField(Launderette, null=True, on_delete= models.SET_NULL)
    description = models.CharField(max_length=500, null=True, blank=True)
    status =models.CharField(max_length=50, blank=True, null=True,choices=StatusChoice2.choices,default=StatusChoice2.PENDING)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.client.name)

class Transactions(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
    launderette = models.ForeignKey(Launderette, null=True, on_delete= models.SET_NULL)
    details = models.CharField(max_length=200, null=True)
    amount = models.FloatField(default=0)
    available_balance = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.client.name)


class Review(models.Model):
    launderette = models.ForeignKey(Launderette, null=True, on_delete= models.SET_NULL)
    client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete= models.SET_NULL)
    rating = models.FloatField(null=True, blank= True)
    review = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.client.name)


class Complaint(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
    subject = models.CharField(max_length=200, null=True)
    complain = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.client.name)

