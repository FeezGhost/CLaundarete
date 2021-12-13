from django.contrib import admin
from .models import *

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_email_verified', 'city', 'isBlocked', 'date_joined')

class LaundererAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_email_verified', 'city', 'isBlocked', 'date_joined')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'launderette', 'status', 'date_created')

class LaunderetteAdmin(admin.ModelAdmin):
    list_display = ('launderer', 'name', 'available_time', 'isBlocked', 'date_joined')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'launderette')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('launderette', 'client', 'rating', 'date')

class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('launderette', 'client', 'date')

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'launderer', 'client', 'date')

admin.site.register(Client, ClientAdmin)
admin.site.register(Transactions)
admin.site.register(Launderer, LaundererAdmin)
admin.site.register(Launderette, LaunderetteAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(ReviewComment, ReviewCommentAdmin)