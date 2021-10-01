from django.http.request import QueryDict
from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .filters import *
from django.core.paginator import Paginator, EmptyPage
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

    launderette = launderer.launderette_set.all()[0]
    totalLaunderette = launderer.launderette_set.all().count()

    reviews = launderette.review_set.all()
    positiveReviews = reviews.filter(rating__gte=2.5).count()
    negativeReviews = reviews.filter(rating__lt=2.5).count()
    totalreviews = reviews.count()
    reviewsRatio = float((positiveReviews/totalreviews)*100)
    
    orders = launderette.order_set.all()
    totalOrders = orders.count()
    newOrders = orders.filter(status = 'pending')
    totalNewOrders = newOrders.count()
    ongoingOrders = orders.filter(status = 'ongoing').order_by('-date_started') 
    finishedOrders = orders.filter(status = 'finished').order_by('-date_end')
    totalOngoingOrders = ongoingOrders.count()
    canceledOrders = orders.filter(status = 'declined')
    acceptedOrders = orders.exclude(status = 'declined').count()
    totalCanceledOrders = canceledOrders.count()
    acceptedOrdersRatio = 100 - float((totalCanceledOrders/totalOrders)*100)

    context = {
        "launderer" : launderer, 
        'totalLaunderette' : totalLaunderette,
        'totalreviews' : totalreviews,
        'positiveReviews' : positiveReviews,
        'negativeReviews' : negativeReviews,
        'newOrders' : totalNewOrders,
        'totalOrders' : totalOrders,
        'totalOngoingOrders' : totalOngoingOrders,
        'ongoingOrders' : ongoingOrders,
        'finishedOrders' : finishedOrders,
        'acceptedOrdersRatio' : acceptedOrdersRatio,
        'acceptedOrders' : acceptedOrders,
        'totalCanceledOrders' : totalCanceledOrders,
        'reviewsRatio' : reviewsRatio
        }
    return render(request,"frontend/dashboardIndex.html",context)


def OngoingOrder(request):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    orders = tLaunderette[0].order_set.all().order_by('-date_started')
    onGoing = orders.filter(status='ongoing')
    ordersfliter = OrderFilter(request.GET, queryset=orders)
    onGoing = ordersfliter.qs
    p  = Paginator(onGoing, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"launderer": launder, 'onGoingOrders' : page, 'ordersfilter':ordersfliter}
    return render(request,"frontend/ongoingOrders.html",context)

def ordersHistory(request):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    orders = tLaunderette[0].order_set.all().order_by('-date_started')
    finished = orders.exclude(status='ongoing').exclude(status='pending')
    ordersfliter = OrderFilter2(request.GET, queryset=orders)
    finished = ordersfliter.qs
    p  = Paginator(finished, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"launderer": launder, 'finisheds' : page, 'ordersfliter': ordersfliter}
    return render(request,"frontend/ordersHistory.html",context)

def ordersRequests(request):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    orders = tLaunderette[0].order_set.all().order_by('-date_started')
    orderequests = orders.filter(status='pending')
    p  = Paginator(orderequests, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"launderer": launder, 'orderRequests' : page}
    return render(request,"frontend/orderRequests.html",context)

def orderRequestProcess(request, pk_id):
    order = Order.objects.get(id = pk_id)
    print(11)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        print(req_status)
        if req_status == 'accept':
            order.status='ongoing'
            orderObj = order.save()
            return redirect('ordersRequest')
        else:
            order.status='declined'
            orderObj = order.save()
            return redirect('ordersRequest')

def orderDetails(request, pk_id):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    order = Order.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'finished':
            order.status='finished'
            orderObj = order.save()
            return redirect('dashboard')
        else:
            order.status='cancel'
            orderObj = order.save()
            return redirect('dashboard')
    context = {"launderer": launder, 'order' : order}
    return render(request,"frontend/orderDetail.html",context)


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
    launderer = request.user.launderer
    launderette = launderer.launderette_set.all()
    reviews = launderette[0].review_set.all()
    reviewsFilters = ReviewFilter(request.GET, queryset=reviews)
    reviews = reviewsFilters.qs
    p  = Paginator(reviews, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'launderer':launderer, 'reviews':page, 'reviewsFilters': reviewsFilters}
    return render(request,"frontend/launderetteReviews.html",context)

def launderetteReviewDetail(request, pk_id):
    launderer = request.user.launderer
    review = Review.objects.get(id=pk_id)
    launderette = launderer.launderette_set.all()
    comments = review.reviewcomment_set.all()
    commentForm = ReviewCommentForm()
    if request.method == "POST":
        commentForm = ReviewCommentForm(request.POST)
        if commentForm.is_valid():
            com = commentForm.cleaned_data.get('comment')
            reviewCommentObject = ReviewComment.objects.create(
                comment = com,
                review = review,
                launderette = launderette[0]
            )
    context = {'launderer':launderer, 'review':review, 'comments': comments, 'commentForm': commentForm }
    return render(request,"frontend/launderetteReviewDetail.html",context)

def deleteComment(request, pk_id):
    reviewComment = ReviewComment.objects.get(id=pk_id)
    if request.method == 'POST':
        reviewComment.delete()
        return redirect('laundaretteReviewDetail', reviewComment.review.id)
    else:
        return redirect('laundaretteReviewDetail', reviewComment.review.id)

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


# Admin Dashboard

def adminDashboardView(request):
    admin = request.user
    context = {"admin": admin}
    return render(request,"frontend/admin/dashboard.html",context)

def adminLaunderersView(request):
    admin = request.user
    launderers = Launderer.objects.all()
    context = {"admin": admin,'launderers': launderers}
    return render(request,"frontend/admin/launderers.html",context)

def adminLaundererDetailView(request, pk_id):
    admin = request.user
    launderer = Launderer.objects.get(id = pk_id)
    launderette = launderer.launderette_set.all()[0]
    context = {"admin": admin,'launderer': launderer, 'launderette': launderette }
    return render(request,"frontend/admin/laundererDetail.html",context)

def laundererRequestProcess(request, pk_id):
    launderer = Launderer.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        print(req_status)
        if req_status == 'block':
            launderer.isBlocked = True
            laundererObj = launderer.save()
            return redirect('adminLaunderers')
        else:
            launderer.isBlocked= False
            laundererObj = launderer.save()
            return redirect('adminLaunderers')


def adminLaunderettesView(request):
    admin = request.user
    launderettes = Launderette.objects.all()
    context = {"admin": admin,'launderettes': launderettes}
    return render(request,"frontend/admin/launderettes.html",context)

def launderetteRequestProcess(request, pk_id):
    launderette = Launderette.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        print(req_status)
        if req_status == 'block':
            launderette.isBlocked = True
            launderetteObj = launderette.save()
            return redirect('adminLaunderettes')
        else:
            launderette.isBlocked= False
            launderetteObj = launderette.save()
            return redirect('adminLaunderettes')

def adminLaunderetteDetailView(request, pk_id):
    admin = request.user
    launderette = Launderette.objects.get(id = pk_id)
    launderer = launderette.launderer
    orders = launderette.order_set.all().order_by('-date_started')
    context = {"admin": admin,'launderette': launderette, 'launderer': launderer, 'orders':orders}
    return render(request,"frontend/admin/launderetteDetail.html",context)


def adminClientsView(request):
    admin = request.user
    clients = Client.objects.all()
    context = {"admin": admin,'clients': clients}
    return render(request,"frontend/admin/clients.html",context)

def adminClientDetailView(request, pk_id):
    admin = request.user
    client = Client.objects.get(id = pk_id)
    orders =client.order_set.all().order_by('-date_created')
    context = {"admin": admin,'client': client,  "orders": orders}
    return render(request,"frontend/admin/clientDetail.html",context)

def clientRequestProcess(request, pk_id):
    client = Client.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        print(req_status)
        if req_status == 'block':
            client.isBlocked = True
            clientObj = client.save()
            return redirect('adminClients')
        else:
            client.isBlocked= False
            clientObj = client.save()
            return redirect('adminClients')


def adminReviewsView(request):
    admin = request.user
    reviews = Review.objects.all()
    context = {"admin": admin,'reviews': reviews}
    return render(request,"frontend/admin/reviews.html",context)

def adminReviewDetail(request, pk_id):
    review = Review.objects.get(id=pk_id)
    comments = review.reviewcomment_set.all()
    context = {'review':review, 'comments': comments}
    return render(request,"frontend/admin/review_details.html",context)


def adminOrdersView(request):
    admin = request.user
    orders = Order.objects.all()
    context = {"admin": admin,'orders': orders}
    return render(request,"frontend/admin/orders.html",context)

def adminOrderDetails(request, pk_id):
    order = Order.objects.get(id = pk_id)
    context = { 'order' : order}
    return render(request,"frontend/admin/order_detail.html",context)


def adminComplaintsView(request):
    admin = request.user
    complaints = Complaint.objects.all()
    context = {"admin": admin,'complaints': complaints}
    return render(request,"frontend/admin/complaints.html",context)