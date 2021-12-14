from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import *
from django.core.paginator import Paginator, EmptyPage
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generateToken
from django.core.mail import EmailMessage, message
from django.conf import settings
import threading
from django.shortcuts import get_object_or_404


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(request, user):
    cuurent_site = get_current_site(request)
    email_subject = "Activate Your Account"
    email_body = render_to_string("frontend/authentication/activate.html",{
        'user': user,
        'domain': cuurent_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })
    email = EmailMessage(
        subject = email_subject,
        body = email_body,
        from_email = settings.EMAIL_HOST_USER,
        to = [user.email],
    )
    if not settings.TESTING:
        EmailThread(email).start()

@unauthenticated_user
def landingpageView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email =request.POST.get('email')
        subject =request.POST.get('subject')
        msg =request.POST.get('message')
        email_body =f"Name: {name}, \nEmail: {email}, \nMessage: {msg}"
        # email_body = "Name: ", name , "\nMessage:\n", msg, "\nUser Email: ", email
        
        email = EmailMessage(
            subject = subject,
            body = email_body,
            from_email = settings.EMAIL_HOST_USER,
            to = [settings.EMAIL_HOST_USER],
        )

        email.send()
        messages.info(request, "Thank You! You email has been delivered")

    return render(request,"frontend/landing-page.html")



@unauthenticated_user
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                messages.error(request, "Admins can't access launderer dashboard")
                return redirect("adminLoginPage")
            elif user.launderer.is_email_verified:
                if user.is_active:
                    login(request, user)
                    greet = "Welcome to the CL Dashboard "+request.user.username
                    messages.info(request, greet)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is inactive or blocked please contact admin')
            else:
                messages.error(request, 'Email is not verified, please check your email inbox')
                return render(request,"frontend/login.html", status=409)
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return render(request,"frontend/login.html", status=409)

    return render(request,"frontend/login.html")

@login_required(login_url="loginPage")
def logoutView(request):
    isStaff = request.user.is_staff
    logout(request)
    messages.info(request, "Hope to see you again!")
    if isStaff:
        return redirect("adminLoginPage")
    return redirect("loginPage")

@unauthenticated_user
def RegisterView(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            fname = form.cleaned_data.get('name')
            city = form.cleaned_data.get('city')
            addres = form.cleaned_data.get('address')
            latitude = float(request.POST.get('lat'))
            longitude = float(request.POST.get('logn'))
            easyp = float(request.POST.get('easypaisa_account'))
            launderer=Launderer.objects.create(
               user=user,
               name=fname,
               city=city,
               address=addres,
               lat= latitude,
               lon = longitude,
               easypaisa_account= easyp
            )
            user = User.objects.get(username=form.cleaned_data.get('username'))
            my_group= Group.objects.get(name='launderer')
            my_group.user_set.add(user)

            send_activation_email(request, user)

            messages.success(request, user.username + ' your account has been created.')
            messages.info(request, 'We sent verification email to your account please check it out!')
            return redirect('loginPage')

        else:
            messages.error(request, "Couldn't create account. Please provide correct information!")
            context = {'form': form}
            return render(request,"frontend/register.html",context, status=409)

    context = {'form': form}
    return render(request,"frontend/register.html",context)

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        launderer = user.launderer
    
    except Exception as e:
        user = None
        launderer = None
    
    if user and launderer and generateToken.check_token(user,token):
        launderer.is_email_verified = True
        launderer.save()
        
        messages,success(request, 'Your Account is now Verified')
        return redirect('loginPage')
    
    return render(request, 'frontend/authentication/activate-failed.html', {'user': user})

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def DashboardView(request):
    launderer = request.user.launderer
    totalLaunderette = launderer.launderette_set.all().count()
    totalreviews = 0
    positiveReviews = 0
    negativeReviews = 0 
    reviewsRatio = 0 
    totalNewOrders = 0
    totalOrders = 0
    totalOngoingOrders = 0
    totalCanceledOrders = 0
    acceptedOrdersRatio = 0
    ongoingOrders = ''
    finishedOrders = ''
    canceledOrders = ''
    acceptedOrders = ''
    if totalLaunderette > 0 :
        launderette = launderer.launderette_set.all()[0]
        if totalLaunderette >0:
            reviews = launderette.review_set.all()
            totalreviews = reviews.count()
            if totalreviews > 0:
                positiveReviews = reviews.filter(rating__gte=2.5).count()
                negativeReviews = reviews.filter(rating__lt=2.5).count()
                reviewsRatio = float((positiveReviews/totalreviews)*100)
        orders = launderette.order_set.all()
        totalOrders = orders.count()
        if totalOrders > 0 :
            newOrders = orders.filter(status = 'pending').order_by('date_created')
            totalNewOrders = newOrders.count()
            ongoingOrders = orders.filter(status = 'ongoing').order_by('-date_started')[:3]
            finishedOrders = orders.filter(status = 'finished').order_by('-date_end')[:3]
            totalOngoingOrders = ongoingOrders.count()
            canceledOrders = orders.filter(status = 'declined')
            acceptedOrders = orders.exclude(status = 'declined').count()
            totalCanceledOrders = canceledOrders.count()
            if totalCanceledOrders > 0 :
                acceptedOrdersRatio =  float((totalCanceledOrders/totalOrders)*100)
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

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def ReportView(request):
    launderer = request.user.launderer
    totalLaunderette = launderer.launderette_set.all().count()
    totalreviews = 0
    positiveReviews = 0
    negativeReviews = 0 
    reviewsRatio = 0 
    totalNewOrders = 0
    totalOrders = 0
    totalOngoingOrders = 0
    totalCanceledOrders = 0
    acceptedOrdersRatio = 0
    ongoingOrders = ''
    finishedOrders = ''
    canceledOrders = ''
    acceptedOrders = ''

    end_date = datetime.date.today().strftime("%m")
    end_dateYear = datetime.date.today().strftime("%Y")
    start_date = launderer.date_joined.date().strftime("%m")
    if totalLaunderette>0:
        end = int(end_date)
        i = int(start_date)
        if i > end:
            i=1
        else:
            i=int(start_date)

        launderette = launderer.launderette_set.all()[0]

        orders = launderette.order_set.all()
        totalOrders = orders.count()
        if totalOrders > 0:
            ordersAccepted = launderette.order_set.all().exclude(status = 'declined').exclude(status = 'pending').exclude(status = 'canceled')
            ordersDeclined = launderette.order_set.all().filter(status = 'declined')
            ordersCanceled = launderette.order_set.all().filter(status = 'canceled')
            acceptedOrdersList = []
            declinedOrdersList = []
            totalOrdersList = []

            reviews = launderette.review_set.all()
            totalreviews = reviews.count()
            positiveReviews = reviews.filter(rating__gte=2.5)
            negativeReviews = reviews.filter(rating__lt=2.5)

            reviews_average = 0.0
            reviews_counter = 0
            reviews_sum = 0

            avgReviewsList = []
            positiveReviewsList = []
            negativeReviewsList = []
            acceptedOrderRatioList = []
            declinedOrderRatioList = []
            positiveReviewsRatioList = []
            negativeReviewsRatioList = []
            totalReviewsList = []
            monthsList = []
            while i <= end:
                fullDate =str(1)+"-"+str(i)+"-"+end_dateYear
                ordersA = ordersAccepted.filter(date_started__month__gte=i,
                                        date_started__month__lt=(i+1)).count()
                acceptedOrdersList.append(ordersA)
                ordersD = ordersDeclined.filter(date_created__month__gte=i,
                                        date_created__month__lt=(i+1)).count()
                
                ordersD += ordersCanceled.filter(date_created__month__gte=i,
                                        date_created__month__lt=(i+1)).count()
                declinedOrdersList.append(ordersD)
                ordersT = orders.filter(date_created__month__gte=i,
                                        date_created__month__lt=(i+1)).count()
                totalOrdersList.append(ordersT)

                acceptedOrderRatio = int(100 - float((ordersD/totalOrders)*100))
                declinedOrderRatio = int(float((ordersD/totalOrders)*100))
                
                reviewsPos = positiveReviews.filter(date__month__gte=i,
                                        date__month__lt=(i+1)).count()
                reviewsneg = negativeReviews.filter(date__month__gte=i,
                                        date__month__lt=(i+1)).count()
                reviewsavg = reviews.filter(date__month__gte=i,
                                        date__month__lt=(i+1))
                totalReviewsList.append(reviewsavg.count())
                positiveReviewsList.append(reviewsPos) 
                negativeReviewsList.append(reviewsneg)
                if totalreviews>0:
                    postiveRatio = int(float((reviewsPos/totalreviews)*100))
                    negativeRatio = int(float((reviewsneg/totalreviews)*100))
                    
                    for review in reviewsavg:
                        reviews_sum += review.rating
                        reviews_counter +=1
                    reviews_average = 100-(reviews_sum/reviews_counter)*10
                    avgReviewsList.append(reviews_average)
                    reviewRatio_average_data = dict(zip(avgReviewsList, avgReviewsList))
                else:
                    postiveRatio = 0
                    negativeRatio = 0

                acceptedOrderRatioList.append(acceptedOrderRatio)
                declinedOrderRatioList.append(declinedOrderRatio)

                positiveReviewsRatioList.append(postiveRatio)
                negativeReviewsRatioList.append(negativeRatio)

                month = datetime.date(1900, i, 1).strftime('%B')
                monthsList.append(month)
                i+=1

            bar_month_data = dict(zip(monthsList,monthsList))
            bar_accept_data = tuple(zip(acceptedOrdersList, acceptedOrdersList))
            bar_decline_data = tuple(zip(declinedOrdersList, declinedOrdersList))
            bar_total_data = tuple(zip(totalOrdersList,totalOrdersList))
            bar_total_data2 = tuple(zip(totalReviewsList,totalReviewsList))
            line_accept_data = tuple(zip(acceptedOrderRatioList, acceptedOrderRatioList))
            line_decline_data = tuple(zip(declinedOrderRatioList, declinedOrderRatioList))
            totalDeclined = ordersDeclined.count()
            totalFinished = launderette.order_set.all().filter(status = 'finished').count()

            reviewbar_accept_data = tuple(zip(positiveReviewsList, positiveReviewsList))
            reviewbar_decline_data = tuple(zip(negativeReviewsList, negativeReviewsList))

            reviewRatio_accept_data = tuple(zip(positiveReviewsRatioList, positiveReviewsRatioList))
            reviewRatio_decline_data = tuple(zip(negativeReviewsRatioList, negativeReviewsRatioList))
            reviewRatio_average_data = tuple(zip(avgReviewsList, avgReviewsList))

            positiveReviews = positiveReviews.count()
            negativeReviews = negativeReviews.count()

            reviewsRatio = float((positiveReviews/totalreviews)*100)
            
            newOrders = orders.filter(status = 'pending').order_by('date_created')
            totalNewOrders = newOrders.count()
            ongoingOrders = orders.filter(status = 'ongoing').order_by('-date_started')[:3]
            finishedOrders = orders.filter(status = 'finished').order_by('-date_end')[:3]
            totalOngoingOrders = ongoingOrders.count()
            canceledOrders = orders.filter(status = 'declined')
            acceptedOrders = orders.exclude(status = 'declined').count()
            totalCanceledOrders = canceledOrders.count()
            if totalCanceledOrders > 0 :
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
                'reviewsRatio' : reviewsRatio,
                'bar_month_data': bar_month_data,
                'bar_accept_data': bar_accept_data,
                'bar_decline_data': bar_decline_data,
                'line_accept_data': line_accept_data,
                'line_decline_data': line_decline_data,
                'totalDeclined':totalDeclined,
                'totalFinished':totalFinished,
                'reviewbar_accept_data': reviewbar_accept_data,
                'reviewbar_decline_data': reviewbar_decline_data,
                'reviewRatio_accept_data': reviewRatio_accept_data,
                'reviewRatio_decline_data': reviewRatio_decline_data,
                'reviewRatio_average_data':  reviewRatio_average_data,
                'bar_total_data':bar_total_data,
                'bar_total_data2':bar_total_data2,
            }
        else:
            context = {
                "launderer" : launderer, 
                'totalLaunderette' : totalLaunderette,
            }
    else:
        context = {
            "launderer" : launderer, 
        }
            
    
    return render(request,"frontend/perfomanceReport.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def OngoingOrder(request):
    launder = request.user.launderer
    serv = ""
    if launder.launderette_set.all().count()>0:
        tLaunderette = launder.launderette_set.all()
        orders = tLaunderette[0].order_set.all().order_by('-date_started')
        if orders.count() > 0:
            if tLaunderette[0].services_set.all():
                serv = tLaunderette[0].services_set.all()
            onGoing = orders.filter(status='ongoing')
            if request.method == 'POST':
                service_id = request.POST.get('service_id')
                service = Services.objects.get(id = int(service_id))
                onGoing = onGoing.filter(services = service)
            ordersfliter = OrderFilter(request.GET, queryset=onGoing)
            onGoing = ordersfliter.qs
            p  = Paginator(onGoing, 20)
            page_num = request.GET.get('page', 1)
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
            context = {"launderer": launder, 'onGoingOrders' : page, 'ordersfilter':ordersfliter,'services': serv}
            return render(request,"frontend/ongoingOrders.html",context)
    context = {"launderer": launder, }
    return render(request,"frontend/ongoingOrders.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def ordersHistory(request):
    launder = request.user.launderer
    serv = ""
    if launder.launderette_set.all().count()>0:
        tLaunderette = launder.launderette_set.all()
        orders = tLaunderette[0].order_set.all().order_by('-date_started')
        if orders.count() > 0:
            if tLaunderette[0].services_set.all():
                serv = tLaunderette[0].services_set.all()
            finished = orders.exclude(status='ongoing').exclude(status='pending')
            if request.method == 'POST':
                finished = orders.exclude(status='ongoing').exclude(status='pending')
                service_title = request.POST.get('service_title')
                service_id = request.POST.get('service_id')
                service = Services.objects.get(id = int(service_id))
                finished = finished.filter(services = service)
            ordersfliter = OrderFilter2(request.GET, queryset=finished)
            finished = ordersfliter.qs
            p  = Paginator(finished, 20)
            page_num = request.GET.get('page', 1)
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
            context = {"launderer": launder, 'finisheds' : page, 'ordersfliter': ordersfliter, 'services': serv}
            return render(request,"frontend/ordersHistory.html",context)
    context = {"launderer": launder, }
    return render(request,"frontend/ordersHistory.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def ordersRequests(request):
    launder = request.user.launderer
    hasOrders =False
    if launder.launderette_set.all().count()>0:
        tLaunderette = launder.launderette_set.all()
        orders = tLaunderette[0].order_set.all().order_by('-date_started')
        if orders.count() > 0:
            orderequests = orders.filter(status='pending')
            hasOrders = bool(orderequests.count() > 0)
            p  = Paginator(orderequests, 10)
            page_num = request.GET.get('page', 1)
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
            context = {"launderer": launder, 'orderRequests' : page, 'hasOrders': hasOrders}
            return render(request,"frontend/orderRequests.html",context)

    context = {"launderer": launder, 'hasOrders': hasOrders}
    return render(request,"frontend/orderRequests.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def orderRequestProcess(request, pk_id):
    order = Order.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'accept':
            order.status='ongoing'
            orderObj = order.save()
            messages.info(request, "Order Accepted")
            return redirect('ordersRequest')
        else:
            order.status='declined'
            orderObj = order.save()
            messages.warning(request, "Order Declined")
            return redirect('ordersRequest')

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def orderDetails(request, pk_id):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    order = Order.objects.get(id = pk_id)
    services = order.services.all()
    haveReview = order.review_set.all().exists()
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'finished':
            order.status='pre-finished'
            orderObj = order.save()
            messages.info(request, "Orders is now in Pre Finished State. Wait for CLient to verify it. You can find this order in orders history.")
            return redirect('ongoingOrders')
        else:
            order.status='cancel'
            orderObj = order.save()
            messages.warning(request, "Orders has been Canceled! you can find this order in orders history.")
            return redirect('ongoingOrders')
    
    if haveReview:
        review = order.review_set.all()[0]
        context = {"launderer": launder, 'order' : order, "review": review, "haveReview": haveReview}
    else:
        context = {"launderer": launder, 'order' : order, "haveReview": haveReview}
    return render(request,"frontend/orderDetail.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def services(request):
    launder = request.user.launderer
    tLaunderette = launder.launderette_set.all()
    serviceForm = ServicesForm()
    totalLaunderette = tLaunderette.count()
    if totalLaunderette > 0:
        launderette = tLaunderette[0]
        if launderette.services_set.all().count()>0:
            services = launderette.services_set.all()
            context = { 'serviceForm': serviceForm, 'launderer' : launder, 'services' : services, 'totalLaunderette' : totalLaunderette }
            return render(request,"frontend/services.html",context)
    else:
        return redirect("launderette")

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
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
            messages.success(request, "Service Edited sucessfully")
            return redirect("services")
        else:
            messages.error(request, "Service Couldn't be edited")
    return render(request,"frontend/servicesEdit.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def servicesDelete(request, pk_id):
    service = Services.objects.get(id=pk_id)
    service.delete()
    messages.success(request, "Service Deleted sucessfully")
    return redirect('services')

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])  
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
            messages.success(request, "Service added sucessfully")
            return redirect("services")

    messages.error(request, "Service couldn't be added")          
    return redirect("services")

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])  
def complaints(request):
    launder = request.user.launderer
    complaints = launder.complaint_set.all().order_by('-date')
    complaintsFilter = ComplaintFilter(request.GET, queryset=complaints)
    complaints = complaintsFilter.qs
    p  = Paginator(complaints, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'launderer' : launder,  "complaints": page, "complaintsFilter": complaintsFilter}
    return render(request,"frontend/complaints.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])  
def complaintDetail(request, pk_id):
    launder = request.user.launderer
    complaint = Complaint.objects.get(id = pk_id)
    context = {'launderer' : launder,  "complaint": complaint}
    return render(request,"frontend/complaintDetail.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])  
def complaintNew(request):
    launder = request.user.launderer
    complaintForm = ComplaintForm()
    if request.method == 'POST':
        complaintForm = ComplaintForm(request.POST)
        print(complaintForm)
        if complaintForm.is_valid():
            sbj = complaintForm.cleaned_data.get('subject')
            comp = complaintForm.cleaned_data.get('complain')
            complaintObj = Complaint.objects.create(
                    launderer = launder,
                    subject = sbj,
                    complain = comp,
            )
            messages.success(request, "Complaint has been submitted!")
            return redirect("complaints")
        else:
            messages.error(request, "Complaiint submission Failed!")  
    context = {'launderer' : launder,  "form": complaintForm}        
    return render(request,"frontend/complaintNew.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
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
                loc = form.cleaned_data.get('location')
                avTime = form.cleaned_data.get('available_time')
                delivery = form.cleaned_data.get('delivery_fee_pkm')
                launderetteObject = Launderette.objects.create(
                    launderer = launder,
                    name = nam,
                    cover_photo = cphoto,
                    location = loc,
                    available_time = avTime,
                    delivery_fee_pkm = delivery
                )
                return redirect("launderette")
                
        return render(request,"frontend/newLaunderette.html",context)
    else :
        context = {'launderer': launder, 'launderette': launderette[0], 'totalLaunderette' : totalLaunderette}
        return render(request,"frontend/launderette.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def launderetteEdit(request):
    launder = request.user.launderer
    launderette = launder.launderette_set.all()
    form = LaunderetteForm(instance= launderette[0])
    if request.method == 'POST':
        form = LaunderetteForm(request.POST, request.FILES, instance=launderette[0])
        if form.is_valid():
            form.save()
            messages.success(request, "Launderette Information updated!.")
            return redirect("launderette")
        else:
            messages.error(request, "Launderette Information couldn't be updated!.")
    context = { 'form': form, 'launderer': launder }
    return render(request,"frontend/launderetteEdit.html",context)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def launderetteReviews(request):
    launderer = request.user.launderer
    if launderer.launderette_set.all().count() > 0:
        launderette = launderer.launderette_set.all()
        reviews = launderette[0].review_set.all().order_by('-date')
        if reviews.count() > 0:
            reviewsFilters = ReviewFilter(request.GET, queryset=reviews)
            reviews = reviewsFilters.qs
            p  = Paginator(reviews, 20)
            page_num = request.GET.get('page', 1)
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
            context = {'launderer':launderer, 'reviews':page, 'reviewsFilters': reviewsFilters}
        else:
            context = {'launderer':launderer,}
        return render(request,"frontend/launderetteReviews.html",context)
    else:
        return redirect("launderette")

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
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

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def deleteComment(request, pk_id):
    reviewComment = ReviewComment.objects.get(id=pk_id)
    if request.method == 'POST':
        reviewComment.delete()
        return redirect('laundaretteReviewDetail', reviewComment.review.id)
    else:
        return redirect('laundaretteReviewDetail', reviewComment.review.id)

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
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

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def changeGeneralInfo(request):
    launderer = request.user.launderer
    if request.method == 'POST':
        form = LaundererForm(request.POST, request.FILES, instance=launderer)
        if form.is_valid():
            form.save()
                
    return redirect("myAccount")

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def changeProfilepic(request):
    launderer = request.user.launderer
    if request.method == 'POST':
        form = LaundererProfilePicForm(request.POST, request.FILES, instance=launderer)
        if form.is_valid():
            form.save()
                
    return redirect("myAccount")

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
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

@login_required(login_url="loginPage")
@allowed_users(allowed_roles=['launderer'])
def changeEmail(request):
    curr_user=request.user
    if request.method == 'POST':
        form = LaundererEmailForm(request.POST, instance= curr_user)
        if form.is_valid():
            form.save()
            
            send_activation_email(request, curr_user)
            messages.info(request, 'We sent verification email to your account please check it out!')
            return redirect('logout')
                
    return redirect("myAccount")


# Admin Dashboard

def adminLoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.info(request, 'Welcome to the Admin Dashboard!')
                return redirect('adminDashboard')
            else:
                messages.info(request, 'Only Admins can login here')
                return render(request,"frontend/admin/login.html", status=409)
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request,"frontend/admin/login.html", status=409)
    return render(request,"frontend/admin/login.html")

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminDashboardView(request):
    admin = request.user
    launderer = Launderer.objects.all()
    laundererTotal = Launderer.objects.all().count()
    launderers = launderer.order_by('-date_joined')[:5]
    launderette = Launderette.objects.all()
    launderetteTotal = launderette.count()
    launderettes = launderette.order_by('-date_joined')[:3]
    client = Client.objects.all()
    clientTotal = client.count()
    clients = client.order_by('-date_joined')[:5]
    order = Order.objects.all()
    orderTotal = order.count()
    orders = order.order_by('-date_created')[:5]
    review = Review.objects.all()
    reviewTotal = review.count()
    reviews = review.order_by('-date')[:5]
    context = {
         "admin": admin,  
         "launderers": launderers, "laundererTotal": laundererTotal,
         "launderettes": launderettes, "launderetteTotal": launderetteTotal,
         "clients": clients, "clientTotal": clientTotal,
         "orders": orders, "orderTotal": orderTotal,
         "reviews": reviews, "reviewTotal": reviewTotal,
        }
    return render(request,"frontend/admin/dashboard.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminLaunderersView(request):
    admin = request.user
    launderers = Launderer.objects.all().order_by('-date_joined')
    laundererFilters = LaundererFilter(request.GET, queryset=launderers)
    launderers = laundererFilters.qs
    p  = Paginator(launderers, 6)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin,'launderers': page,  "laundererFilters":laundererFilters}
    return render(request,"frontend/admin/launderers.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminLaundererDetailView(request, pk_id):
    admin = request.user
    launderer = Launderer.objects.get(id = pk_id)
    if launderer.launderette_set.all().count() > 0:
        launderette = launderer.launderette_set.all()[0]
        context = {"admin": admin,'launderer': launderer, 'launderette': launderette }
        return render(request,"frontend/admin/laundererDetail.html",context)
    else :
        return redirect('adminLaunderers')

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def laundererRequestProcess(request, pk_id):
    launderer = Launderer.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'block':
            launderer.isBlocked = True
            launderer.user.is_active = False
            launderer.user.save()
            laundererObj = launderer.save()
            msg = launderer.name, ' has been blocked'
            messages.warning(request, msg)
            return redirect('adminLaunderers')
        else:
            launderer.isBlocked= False
            launderer.user.is_active = True
            launderer.user.save()
            laundererObj = launderer.save()
            msg = launderer.name, ' has been unblocked'
            messages.warning(request, msg)
            return redirect('adminLaunderers')

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminLaunderettesView(request):
    admin = request.user
    launderettes = Launderette.objects.all().order_by('-date_joined')
    launderetteFilters = LaunderetteFilter(request.GET, queryset=launderettes)
    launderettes = launderetteFilters.qs
    p  = Paginator(launderettes, 6)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin,'launderettes': page, "launderetteFilters": launderetteFilters}
    return render(request,"frontend/admin/launderettes.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def launderetteRequestProcess(request, pk_id):
    launderette = Launderette.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'block':
            launderette.isBlocked = True
            launderetteObj = launderette.save()
            msg = launderette.name, '  has been unblocked!'
            messages.warning(request, msg)
            return redirect('adminLaunderettes')
        else:
            launderette.isBlocked= False
            launderetteObj = launderette.save()
            msg = launderette.name, '  has been unblocked!'
            messages.warning(request, msg)
            return redirect('adminLaunderettes')

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminLaunderetteDetailView(request, pk_id):
    admin = request.user
    launderette = Launderette.objects.get(id = pk_id)
    launderer = launderette.launderer
    orders = launderette.order_set.all().order_by('-date_started')
    context = {"admin": admin,'launderette': launderette, 'launderer': launderer, 'orders':orders}
    return render(request,"frontend/admin/launderetteDetail.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminClientsView(request):
    admin = request.user
    clients = Client.objects.all().order_by('-date_joined')
    clientFilters = ClientFilter(request.GET, queryset=clients)
    clients = clientFilters.qs
    p  = Paginator(clients, 6)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin, 'clients': page, 'clientFilters':clientFilters}
    return render(request,"frontend/admin/clients.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminClientDetailView(request, pk_id):
    admin = request.user
    client = Client.objects.get(id = pk_id)
    orders =client.order_set.all().order_by('-date_created')
    context = {"admin": admin,'client': client,  "orders": orders}
    return render(request,"frontend/admin/clientDetail.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def clientRequestProcess(request, pk_id):
    client = Client.objects.get(id = pk_id)
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'block':
            client.isBlocked = True
            client.user.is_active = False
            client.user.save()
            clientObj = client.save()
            msg = client.name, ' has been blocked'
            messages.warning(request, msg)
            return redirect('adminClients')
        else:
            client.isBlocked= False
            client.user.is_active = True
            client.user.save()
            clientObj = client.save()
            msg = client.name, ' has been unblocked'
            messages.warning(request, msg)
            return redirect('adminClients')

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminReviewsView(request):
    admin = request.user
    reviews = Review.objects.all().order_by('-date')
    reviewsFilters = ReviewFilter(request.GET, queryset=reviews)
    reviews = reviewsFilters.qs
    p  = Paginator(reviews, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin,'reviews': page, 'reviewsFilters': reviewsFilters}
    return render(request,"frontend/admin/reviews.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminReviewDetail(request, pk_id):
    admin = request.user
    review = Review.objects.get(id=pk_id)
    comments = review.reviewcomment_set.all()
    context = {"admin": admin, 'review':review, 'comments': comments}
    return render(request,"frontend/admin/review_details.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminOrdersView(request):
    admin = request.user
    orders = Order.objects.all().order_by('-date_started')
    
    ordersfliter = OrderFilter(request.GET, queryset=orders)
    orders = ordersfliter.qs
    p  = Paginator(orders, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin,'orders': page,'ordersfilter':ordersfliter}
    return render(request,"frontend/admin/orders.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminOrderDetails(request, pk_id):
    admin = request.user
    order = Order.objects.get(id = pk_id)
    haveReview = order.review_set.all().exists()
    if request.method == 'POST' :
        req_status = request.POST.get('statusField')
        if req_status == 'finished':
            order.status='finished'
            orderObj = order.save()
            messages.info(request, "Orders is has been Finished. You can find this order in orders history.")
        else:
            order.status='cancel'
            orderObj = order.save()
            messages.warning(request, "Orders has been Canceled! you can find this order in orders history.")
    
    if haveReview:
        review = order.review_set.all()[0]
        context = {"admin": admin, 'order' : order, "review": review, "haveReview": haveReview}
    else:
        context = {"admin": admin, 'order' : order, "haveReview": haveReview}
    return render(request,"frontend/admin/order_detail.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminComplaintsView(request):
    admin = request.user
    complaints = Complaint.objects.all().order_by('-date')
    complaintsFilter = ComplaintFilter(request.GET, queryset=complaints)
    complaints = complaintsFilter.qs
    p  = Paginator(complaints, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"admin": admin, 'complaints': page, "complaintsFilter": complaintsFilter}
    return render(request,"frontend/admin/complaints.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def adminComplaintsDetailView(request, pk_id):
    admin = request.user
    complaint = Complaint.objects.get(id=pk_id)
    form = ComplaintForm(instance= complaint)
    if request.method == 'POST':
        res = request.POST.get('response')
        complaint.status='resolved'
        complaint.response= res
        complaint.save()
        messages.success(request, "Complaint has been Responded!")
        return  redirect("adminComplaints")
    context = {"admin": admin, 'complaint':complaint, 'form': form}
    return render(request,"frontend/admin/complaintDetail.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def AdminLaunderetePerfomanceView(request, pk_id):
    admin = request.user
    launderette = get_object_or_404(Launderette, id=pk_id)
    totalreviews = 0
    positiveReviews = 0
    negativeReviews = 0 
    reviewsRatio = 0 
    totalNewOrders = 0
    totalOrders = 0
    totalOngoingOrders = 0
    totalCanceledOrders = 0
    acceptedOrdersRatio = 0
    ongoingOrders = ''
    finishedOrders = ''
    canceledOrders = ''
    acceptedOrders = ''

    end_date = datetime.date.today().strftime("%m")
    end_dateYear = datetime.date.today().strftime("%Y")
    start_date = launderette.date_joined.date().strftime("%m")

    end = int(end_date)
    i = int(start_date)
    if i > end:
        i=1
    else:
        i=int(start_date)


    orders = launderette.order_set.all()
    totalOrders = orders.count()
    if totalOrders > 0:
        ordersAccepted = launderette.order_set.all().exclude(status = 'declined').exclude(status = 'pending').exclude(status = 'canceled')
        ordersDeclined = launderette.order_set.all().filter(status = 'declined')
        ordersCanceled = launderette.order_set.all().filter(status = 'canceled')
        acceptedOrdersList = []
        declinedOrdersList = []
        totalOrdersList = []

        reviews = launderette.review_set.all()
        totalreviews = reviews.count()
        positiveReviews = reviews.filter(rating__gte=2.5)
        negativeReviews = reviews.filter(rating__lt=2.5)

        reviews_average = 0.0
        reviews_counter = 0
        reviews_sum = 0

        avgReviewsList = []
        positiveReviewsList = []
        negativeReviewsList = []
        acceptedOrderRatioList = []
        declinedOrderRatioList = []
        positiveReviewsRatioList = []
        negativeReviewsRatioList = []
        monthsList = []
        while i <= end:
            fullDate =str(1)+"-"+str(i)+"-"+end_dateYear
            ordersA = ordersAccepted.filter(date_started__month__gte=i,
                                    date_started__month__lt=(i+1)).count()
            acceptedOrdersList.append(ordersA)
            ordersD = ordersDeclined.filter(date_created__month__gte=i,
                                    date_created__month__lt=(i+1)).count()
            
            ordersD += ordersCanceled.filter(date_created__month__gte=i,
                                    date_created__month__lt=(i+1)).count()
            declinedOrdersList.append(ordersD)
            ordersT = orders.filter(date_created__month__gte=i,
                                    date_created__month__lt=(i+1)).count()
            totalOrdersList.append(ordersT)

            acceptedOrderRatio = int(100 - float((ordersD/totalOrders)*100))
            declinedOrderRatio = int(float((ordersD/totalOrders)*100))
            
            reviewsPos = positiveReviews.filter(date__month__gte=i,
                                    date__month__lt=(i+1)).count()
            reviewsneg = negativeReviews.filter(date__month__gte=i,
                                    date__month__lt=(i+1)).count()
            reviewsavg = reviews.filter(date__month__gte=i,
                                    date__month__lt=(i+1))
            positiveReviewsList.append(reviewsPos) 
            negativeReviewsList.append(reviewsneg)
            if totalreviews>0:
                postiveRatio = int(float((reviewsPos/totalreviews)*100))
                negativeRatio = int(float((reviewsneg/totalreviews)*100))
                
                for review in reviewsavg:
                    reviews_sum += review.rating
                    reviews_counter +=1
                reviews_average =100- (reviews_sum/reviews_counter)*10
                avgReviewsList.append(reviews_average)
                reviewRatio_average_data = dict(zip(avgReviewsList, avgReviewsList))
            else:
                postiveRatio = 0
                negativeRatio = 0

            acceptedOrderRatioList.append(acceptedOrderRatio)
            declinedOrderRatioList.append(declinedOrderRatio)

            positiveReviewsRatioList.append(postiveRatio)
            negativeReviewsRatioList.append(negativeRatio)

            month = datetime.date(1900, i, 1).strftime('%B')
            monthsList.append(month)
            i+=1

        bar_month_data = dict(zip(monthsList,monthsList))
        bar_accept_data = tuple(zip(acceptedOrdersList, acceptedOrdersList))
        bar_decline_data = tuple(zip(declinedOrdersList, declinedOrdersList))
        bar_total_data = tuple(zip(totalOrdersList,totalOrdersList))
        line_accept_data = tuple(zip(acceptedOrderRatioList, acceptedOrderRatioList))
        line_decline_data = tuple(zip(declinedOrderRatioList, declinedOrderRatioList))
        totalDeclined = ordersDeclined.count()
        totalFinished = launderette.order_set.all().filter(status = 'finished').count()

        reviewbar_accept_data = tuple(zip(positiveReviewsList, positiveReviewsList))
        reviewbar_decline_data = tuple(zip(negativeReviewsList, negativeReviewsList))

        reviewRatio_accept_data = tuple(zip(positiveReviewsRatioList, positiveReviewsRatioList))
        reviewRatio_decline_data = tuple(zip(negativeReviewsRatioList, negativeReviewsRatioList))
        reviewRatio_average_data = tuple(zip(avgReviewsList, avgReviewsList))

        positiveReviews = positiveReviews.count()
        negativeReviews = negativeReviews.count()

        reviewsRatio = float((positiveReviews/totalreviews)*100)
        
        newOrders = orders.filter(status = 'pending').order_by('date_created')
        totalNewOrders = newOrders.count()
        ongoingOrders = orders.filter(status = 'ongoing').order_by('-date_started')[:3]
        finishedOrders = orders.filter(status = 'finished').order_by('-date_end')[:3]
        totalOngoingOrders = ongoingOrders.count()
        canceledOrders = orders.filter(status = 'declined')
        acceptedOrders = orders.exclude(status = 'declined').count()
        totalCanceledOrders = canceledOrders.count()
        if totalCanceledOrders > 0 :
            acceptedOrdersRatio = 100 - float((totalCanceledOrders/totalOrders)*100)
        context = {"admin": admin, 
            'launderette' : launderette,
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
            'reviewsRatio' : reviewsRatio,
            'bar_month_data': bar_month_data,
            'bar_accept_data': bar_accept_data,
            'bar_decline_data': bar_decline_data,
            'line_accept_data': line_accept_data,
            'line_decline_data': line_decline_data,
            'totalDeclined':totalDeclined,
            'totalFinished':totalFinished,
            'reviewbar_accept_data': reviewbar_accept_data,
            'reviewbar_decline_data': reviewbar_decline_data,
            'reviewRatio_accept_data': reviewRatio_accept_data,
            'reviewRatio_decline_data': reviewRatio_decline_data,
            'reviewRatio_average_data':  reviewRatio_average_data,
            'bar_total_data':bar_total_data,
        }
    else:
        context = {"admin": admin, 
            'launderette' : launderette,
        }

    return render(request,"frontend/admin/launderetteDetailPerfomance.html",context)

@login_required(login_url="adminLoginPage")
@allowed_users(allowed_roles=['admin'])
def AdminReportView(request):
    admin = request.user
    users = User.objects.all()
    launderers = Launderer.objects.all()
    clients = Client.objects.all()
    launderettes = Launderette.objects.all()
    orders = Order.objects.all()
    complaints = Complaint.objects.all()
    complaintsResolved = complaints.filter(status = 'resolved')
    complaintsUnresolved = complaints.filter(status = 'unresolved')
    complaintsClosed = complaints.filter(status = 'closed')

    totalUsers = users.count()
    totalLaunderers = launderers.count()
    totalClients = clients.count()
    totalLaunderettes = launderettes.count()
    totalOrders = orders.count()
    totalComplaints = complaints.count()
    totalComplaintsResolved = complaintsResolved.count()
    totalComplaintsUnresolved = complaintsUnresolved.count()
    totalComplaintsClosed = complaintsClosed.count()
    
    usersList = []
    launderersList = []
    clientsList = []
    launderettesList = []
    ordersList = []
    complaintsList = []
    complaintsResolvedList = []
    complaintsUnresolvedList = []
    monthsList = []
    dummyList = []
    dummyValue = 0

    end_date = datetime.date.today().strftime("%m")
    end_dateYear = datetime.date.today().strftime("%Y")
    start_date = 8
    end = int(end_date)
    i = int(start_date)
    if i > end:
        i=1
    else:
        i=int(start_date)

    while i<=end:
        order = orders.filter(date_started__month__gte=i, date_started__month__lt=(i+1)).count()
        ordersList.append(order)

        complaint = complaints.filter(date__month__gte=i, date__month__lt=(i+1)).count()
        complaintsList.append(complaint)
         
        complaintRsolved = complaintsResolved.filter(date__month__gte=i, date__month__lt=(i+1)).count()
        complaintsResolvedList.append(complaintRsolved)

        complaintUnresolved = complaintsUnresolved.filter(date__month__gte=i, date__month__lt=(i+1)).count()
        complaintsUnresolvedList.append(complaintUnresolved)

        user = users.filter(date_joined__month__gte=i, date_joined__month__lt=(i+1)).count()
        if user < 1 or user == None:
            user = 0
        usersList.append(user)

        client = clients.filter(date_joined__month__gte=i, date_joined__month__lt=(i+1)).count()
        if client < 1 or client == None:
            client = 0
            
        clientsList.append(client)
        
        launderer = launderers.filter(date_joined__month__gte=i, date_joined__month__lt=(i+1)).count()
        if launderer < 1 or launderer == None:
            launderer = 0
            
        launderersList.append(launderer)

        launderette = launderettes.filter(date_joined__month__gte=i, date_joined__month__lt=(i+1)).count()
        if launderette < 1 or launderette == None:
            launderette = 0
            
        launderettesList.append(launderette)

        month = datetime.date(1900, i, 1).strftime('%B')
        monthsList.append(month)

        dummyList.append(dummyValue)
        dummyValue+=1

        i+=1
    
    line_month_data = dict(zip(monthsList,monthsList))
    line_users_data = tuple(zip(dummyList, usersList))
    line_clients_data = tuple(zip(dummyList, clientsList))
    line_launderers_data = tuple(zip(dummyList, launderersList))
    line_launderettes_data = tuple(zip(dummyList, launderettesList))

    line_complaints_data = tuple(zip(dummyList, complaintsList))
    bar_complaints_resolved_data = tuple(zip(dummyList, complaintsResolvedList))
    bar_complaints_unresolved_data = tuple(zip(dummyList, complaintsUnresolvedList))
    
    context = {"admin": admin,
        'line_clients_data': line_clients_data,
        'line_month_data': line_month_data,
        'line_launderettes_data': line_launderettes_data,
        'line_users_data': line_users_data,
        'line_launderers_data': line_launderers_data,

        'totalUsers': totalUsers,
        'totalClients': totalClients,
        'totalLaunderers': totalLaunderers,
        'totalLaunderettes': totalLaunderettes,
        'totalComplaints': totalComplaints,
        'totalOrders': totalOrders,
        'totalComplaintsResolved': totalComplaintsResolved,
        'totalComplaintsUnresolved': totalComplaintsUnresolved,
        
        'line_complaints_data': line_complaints_data,
        'bar_complaints_resolved_data': bar_complaints_resolved_data,
        'bar_complaints_unresolved_data': bar_complaints_unresolved_data
    }

    return render(request,"frontend/admin/perfomance_report.html", context)

