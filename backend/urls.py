from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name="loginPage"),
    path('', views.logoutView, name="logout"),
    path('register/', views.RegisterView, name="registerPage"),
    path('dashboard/', views.DashboardView, name="dashboard"),
    path('dashboard/orders/ongoing/', views.OngoingOrder, name="ongoingOrders"),
    path('dashboard/orders/history/', views.ordersHistory, name="ordersHistory"),
    path('dashboard/orders/requests/', views.ordersRequests, name="ordersRequest"),
    path('dashboard/orders/requests/<str:pk_id>/', views.orderRequestProcess, name="orderRequestProcess"),
    path('dashboard/orders/detail/<str:pk_id>/', views.orderDetails, name="orderDetail"),
    path('dashboard/services/', views.services, name="services"),
    path('dashboard/services/edit/<str:pk_id>/', views.servicesEdit, name="editServices"),
    path('dashboard/services/delete/<str:pk_id>/', views.servicesDelete, name="deleteServices"),
    path('dashboard/services/new/', views.servicesNew, name="newService"),
    path('dashboard/launderette/', views.launderette, name="launderette"),
    path('dashboard/launderette/edit', views.launderetteEdit, name="editlaunderette"),
    path('dashboard/launderette/reviews', views.launderetteReviews, name="laundaretteReviews"),
    path('dashboard/launderette/reviews/detail/<str:pk_id>/', views.launderetteReviewDetail, name="laundaretteReviewDetail"),
    path('dashboard/account/', views.laundererAccount, name="myAccount"),
    path('changeemail/', views.changeEmail, name="changeEmail"),
    path('generalinfo/', views.changeGeneralInfo, name="generalInfo"),
    path('profilepic/', views.changeProfilepic, name="profilepic"),
    path('changepass/', views.changePassword, name="changepass"),

]
