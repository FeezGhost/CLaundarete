from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# from .decorators import  unauthenticated_user, allowed_users,admin_only

# Create your views here.

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request,"frontend/login.html")

def logoutView(request):
    logout(request)
    return redirect("loginPage")

def RegisterView(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            fname = form.cleaned_data.get('name')
            launderer=Launderer.objects.create(
               user=user,
               name=fname,
            )
            myuser = User.objects.get(username=form.cleaned_data.get('username'))
            my_group= Group.objects.get(name='launderer')
            my_group.user_set.add(myuser)

            messages.success(request, 'Account has been created for ' + fname)
            login(request, user)
            return redirect('dashboard')

    context = {'form': form}
    return render(request,"frontend/register.html",context)

def DashboardView(request):
    launderer = request.user.launderer
    totalLaunderette = launderer.launderette_set.all().count()
    context = {"launderer": launderer, 'totalLaunderette': totalLaunderette}
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
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    launderette = tLaunderette[0]
    totalLaunderette = tLaunderette.count()
    serviceForm = ServicesForm()
    services = launderette.services_set.all()
    print(services)
    context = { 'serviceForm': serviceForm, 'launderer' : launder, 'services' : services, 'totalLaunderette' : totalLaunderette }
    return render(request,"frontend/services.html",context)

def servicesEdit(request, pk_id):
    launder = request.user.launderer
    totalLaunderette = launder.launderette_set.all().count()
    service = Services.objects.get(id=pk_id)
    serviceForm = ServicesForm(instance= service)
    context = {'serviceForm': serviceForm, 'launderer' : launder, 'totalLaunderette' : totalLaunderette}
    if request.method == 'POST':
        serviceForm = ServicesForm(request.POST, request.FILES, instance=service)
        if serviceForm.is_valid():
            serviceForm.save()
            return redirect("services")
    return render(request,"frontend/servicesEdit.html",context)

def servicesDelete(request, pk_id):
    service = Services.objects.get(id=pk_id)
    service.delete()
    return redirect('services')
   
def servicesNew(request):
    launder = request.user.launderer
    totalLaunderette = launder.launderette_set.all()
    launderette = totalLaunderette[0]
    if request.method == 'POST':
        serviceForm = ServicesForm(request.POST)
        if serviceForm.is_valid():
            name = serviceForm.cleaned_data.get('title')
            pr = serviceForm.cleaned_data.get('price')
            serviceObject = Services.objects.create(
                    launderette = launderette,
                    title = name,
                    price = pr,
                )
            print(serviceObject)
                
    return redirect("services")

def launderette(request):
    launder = request.user.launderer
    launderette = launder.launderette_set.all()
    totalLaunderette = launderette.count()
    launderetteForm = LaunderetteForm()
    if totalLaunderette == 0 :
        context = { 'launderer': launder, 'launderetteForm': launderetteForm, 'totalLaunderette' : totalLaunderette }
        if request.method == 'POST':
            form = LaunderetteForm(request.POST, request.FILES)
            if form.is_valid():
                nam = form.cleaned_data.get('name')
                cphoto = form.cleaned_data.get('cover_photo')
                print(cphoto)
                loc = form.cleaned_data.get('location')
                avTime = form.cleaned_data.get('available_time')
                launderetteObject = Launderette.objects.create(
                    launderer = launder,
                    name = nam,
                    cover_photo = cphoto,
                    location = loc,
                    available_time = avTime,
                )
                print(launderetteObject)
                return redirect("launderette")
                
        return render(request,"frontend/newLaunderette.html",context)
    else :
        context = {'launderer': launder, 'launderette': launderette[0], 'totalLaunderette' : totalLaunderette}
        return render(request,"frontend/launderette.html",context)

def launderetteEdit(request):
    launder = request.user.launderer
    launderette = launder.launderette_set.all()
    form = LaunderetteForm(instance= launderette[0])
    if request.method == 'POST':
        form = LaunderetteForm(request.POST, request.FILES, instance=launderette[0])
        if form.is_valid():
            form.save()
            return redirect("launderette")
    context = { 'form': form }
    return render(request,"frontend/launderetteEdit.html",context)

def launderetteReviews(request):
    context = {}
    return render(request,"frontend/launderetteReviews.html",context)

def launderetteReviewDetail(request):
    context = {}
    return render(request,"frontend/launderetteReviewDetail.html",context)

def laundererAccount(request):
    launderer = request.user.launderer
    totalLaunderette = launderer.launderette_set.all().count()
    curr_user=request.user
    form = LaundererForm(instance= launderer)
    profilepicform = LaundererProfilePicForm(instance= launderer)
    passwordform = PasswordChangeForm(curr_user)
    emailform = LaundererEmailForm(instance= curr_user)
    context = {"launderer": launderer, "form": form,  'passwordform':passwordform,  'profilepicform':profilepicform, 'emailform': emailform, 'totalLaunderette' : totalLaunderette }
    return render(request,"frontend/profile.html",context)

@login_required(login_url="login")
def changeGeneralInfo(request):
    launderer = request.user.launderer
    if request.method == 'POST':
        form = LaundererForm(request.POST, request.FILES, instance=launderer)
        if form.is_valid():
            form.save()
                
    return redirect("myAccount")

@login_required(login_url="login")
def changeProfilepic(request):
    launderer = request.user.launderer
    if request.method == 'POST':
        form = LaundererProfilePicForm(request.POST, request.FILES, instance=launderer)
        if form.is_valid():
            form.save()
                
    return redirect("myAccount")


@login_required(login_url="login")
def changePassword(request):
    if request.method == 'POST':
        passwordform = PasswordChangeForm(request.user, request.POST)
        if passwordform.is_valid():
            user = passwordform.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
  
    
    return redirect('myAccount')

def changeEmail(request):
    curr_user=request.user
    if request.method == 'POST':
        form = LaundererEmailForm(request.POST, instance= curr_user)
        if form.is_valid():
            form.save()
                
    return redirect("myAccount")
