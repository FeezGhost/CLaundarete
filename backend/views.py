from django.shortcuts import render,redirect
# from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .decorators import  unauthenticated_user, allowed_users,admin_only

# Create your views here.

def loginView(request):
    context = {}
    return render(request,"frontend/login.html",context)


def RegisterView(request):
    context = {}
    return render(request,"frontend/register.html",context)

def DashboardView(request):
    context = {}
    return render(request,"frontend/dashboardIndex.html",context)


def OngoingOrder(request):
    context = {}
    return render(request,"frontend/ongoingOrders.html",context)

def ordersHistory(request):
    context = {}
    return render(request,"frontend/ordersHistory.html",context)


def ordersRequests(request):
    context = {}
    return render(request,"frontend/orderRequests.html",context)


def services(request):
    context = {}
    return render(request,"frontend/services.html",context)

def servicesEdit(request):
    context = {}
    return render(request,"frontend/servicesEdit.html",context)

def servicesNew(request):
    context = {}
    return render(request,"frontend/servicesNew.html",context)

def launderette(request):
    context = {}
    return render(request,"frontend/launderette.html",context)

def launderetteEdit(request):
    context = {}
    return render(request,"frontend/launderetteEdit.html",context)

def launderetteReviews(request):
    context = {}
    return render(request,"frontend/launderetteReviews.html",context)

def launderetteReviewDetail(request):
    context = {}
    return render(request,"frontend/launderetteReviewDetail.html",context)

def laundererAccount(request):
    context = {}
    return render(request,"frontend/profile.html",context)
