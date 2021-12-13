from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landingpageView, name="homepage"),

    # Launderer Dashboard urls
    path('login/', views.loginView, name="loginPage"),
    path('register/', views.RegisterView, name="registerPage"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="frontend/authentication/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="frontend/authentication/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="frontend/authentication/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="frontend/authentication/password_reset_done.html"), name="password_reset_complete"),

    path('dashboard/', views.DashboardView, name="dashboard"),

    path('dashboard/report/', views.ReportView, name="Report"),

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
    path('dashboard/launderette/edit/', views.launderetteEdit, name="editlaunderette"),
    path('dashboard/launderette/reviews/', views.launderetteReviews, name="laundaretteReviews"),

    path('dashboard/complaints/', views.complaints, name="complaints"),
    path('dashboard/complaints/new/', views.complaintNew, name="newComplaint"),
    path('dashboard/complaints/details/<str:pk_id>/', views.complaintDetail, name="complaintDetail"),

    path('dashboard/launderette/reviews/detail/<str:pk_id>/', views.launderetteReviewDetail, name="laundaretteReviewDetail"),
    path('dashboard/launderette/reviews/detail/delete/<str:pk_id>/', views.deleteComment, name="deleteComment"),

    path('dashboard/account/', views.laundererAccount, name="myAccount"),
    path('dashboard/account/changeemail/', views.changeEmail, name="changeEmail"),
    path('dashboard/account/generalinfo/', views.changeGeneralInfo, name="generalInfo"),
    path('dashboard/account/profilepic/', views.changeProfilepic, name="profilepic"),
    path('dashboard/account/changepass/', views.changePassword, name="changepass"),
    
    path('logout/', views.logoutView, name="logout"),

    # Admin Dashboard urls
    
    path('cladmin/', views.adminLoginView, name="adminLoginPage"),
    path('admindashboard/', views.adminDashboardView, name="adminDashboard"),

    path('admindashboard/launderers/', views.adminLaunderersView, name="adminLaunderers"),
    path('admindashboard/launderers/<str:pk_id>/', views.laundererRequestProcess, name="laundererRequestProcess"),
    path('admindashboard/launderer/details/<str:pk_id>/', views.adminLaundererDetailView, name="adminLaundererDetail"),

    path('admindashboard/launderettes/', views.adminLaunderettesView, name="adminLaunderettes"),
    path('admindashboard/launderettes/<str:pk_id>/', views.launderetteRequestProcess, name="launderetteRequestProcess"),
    path('admindashboard/launderette/details/<str:pk_id>/', views.adminLaunderetteDetailView, name="adminLaunderetteDetail"),

    path('admindashboard/clients/', views.adminClientsView, name="adminClients"),
    path('admindashboard/clients/<str:pk_id>/', views.clientRequestProcess, name="clientRequestProcess"),
    path('admindashboard/clients/details/<str:pk_id>/', views.adminClientDetailView, name="adminClientDetail"),

    path('admindashboard/reviews/', views.adminReviewsView, name="adminReviews"),
    path('admindashboard/reviews/details/<str:pk_id>/', views.adminReviewDetail, name="adminReviewDetail"),

    path('admindashboard/orders/', views.adminOrdersView, name="adminOrders"),
    path('admindashboard/orders/detail/<str:pk_id>/', views.adminOrderDetails, name="adminOrderDetails"),

    path('admindashboard/complaints/', views.adminComplaintsView, name="adminComplaints"),
    path('admindashboard/complaints/detail/<str:pk_id>/', views.adminComplaintsDetailView, name="adminComplaintsDetail"),

    path('admindashboard/analytics/', views.AdminReportView, name="AdminReports"),
    path('admindashboard/analytics/launderette/<str:pk_id>/', views.AdminLaunderetePerfomanceView, name="AdminLaunderetePerfomance"),
]
