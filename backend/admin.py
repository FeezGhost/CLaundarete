from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Transactions)
admin.site.register(Launderer)
admin.site.register(Launderette)
admin.site.register(Order)
admin.site.register(Services)
admin.site.register(Review)
admin.site.register(Complaint)
admin.site.register(ReviewComment)