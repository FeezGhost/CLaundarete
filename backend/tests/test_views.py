from django.contrib.auth.models import User, Group
from utils.setup_test import TestSetup
from django.urls import reverse
from backend.models import Launderer, Launderette, Services, Order,  Complaint,ReviewComment, Client
from backend.forms import ServicesForm, ComplaintForm

class TestRegisterLaundererView(TestSetup):

    def test_should_show_register_page(self):
        response = self.client.get(reverse('registerPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontend/register.html")

    def test_should_signup_user(self):
        launderer = self.create_test_launderer()
        Group.objects.create(name='launderer')
        data = {
            "username": "usertester1212",
            "email": "emailtester@gmail.com",
            "password1": "passweod22",
            "password2": "passweod22",
            "name" : launderer.name,
            "city" : launderer.city,
            "address": launderer.address,
            "lat":  launderer.lat,
            "logn" : launderer.lon,
        }
        users = User.objects.all().count()
        launderers = Launderer.objects.all().count()

        response = self.client.post(reverse("registerPage"), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(users, 1)
        self.assertEquals(launderers, 1)

    def test_should_not_signup_user_with_taken_username(self):

        self.user = {
            "username": "username",
            "email": "email@hmail2.com",
            "password": "password",
            "password2": "password"

        }
        response = self.client.post(reverse("registerPage"), self.user)
        self.assertEquals(response.status_code, 409)

class TestLoginView(TestSetup):

    def test_should_show_login_page(self):
        response = self.client.get(reverse('loginPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontend/login.html")

    def test_should_login_launderer_successfully(self):
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        })

        self.assertEquals(response.status_code, 302)

    def test_should_not_login_unverified_launderer(self):
        launderer = self.create_test_launderer()
        user = launderer.user
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        })
        self.assertEquals(response.status_code, 409)

    def test_should_show_reset_password_page(self):
        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontend/authentication/password_reset.html")

    def test_should_show_password_reset_done_page(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontend/authentication/password_reset_sent.html")
        
    # def test_should_show_password_reset_confirm_page(self):
    #     response = self.client.get(reverse('password_reset_confirm'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "frontend/authentication/password_reset_form.html")

    def test_should_show_password_reset_complete_page(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontend/authentication/password_reset_done.html")

    # def test_should_not_signup_user_with_taken_email(self):

    #     self.user = {
    #         "username": "username1",
    #         "email": "email@hmail2.com",
    #         "password": "password",
    #         "password2": "password"
    #     }

    #     self.test_user2 = {
    #         "username": "username11",
    #         "email": "email@hmail2.com",
    #         "password": "password",
    #         "password2": "password"
    #     }

    #     self.client.post(reverse("registerPage"), self.user)
    #     response = self.client.post(reverse("registerPage"), self.test_user2)
    #     self.assertEquals(response.status_code, 409)

class TestLogoutView(TestSetup):
    
    def test_should_logout_launderer_successfully(self):
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        })

        self.assertEquals(response.status_code, 302)

        response2 = self.client.get(reverse('logout'), follow=True)
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/login.html")

    def test_should_logout_admin_successfully(self):
        user = self.create_test_user()
        user.is_staff = True
        user.save() 
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        })

        self.assertEquals(response.status_code, 302)

        response2 = self.client.get(reverse('logout'), follow=True)
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/admin/login.html")

class TestLaundererDashboardView(TestSetup):

    def test_should_show_dashboard_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(response.redirect_chain[0][0], follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertTemplateUsed(response2, "frontend/dashboardIndex.html")

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_dashboard_anyonmous_user(self):
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_dashboard_admin(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='admin')
        my_group= Group.objects.get(name='admin')
        my_group.user_set.add(user)
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

class TestLaundererReportView(TestSetup):

    def test_should_show_report_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("Report"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertTemplateUsed(response2, "frontend/perfomanceReport.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_check_report_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("Report"), follow=True)

        self.assertTemplateUsed(response2, "frontend/perfomanceReport.html")

    def test_should_not_show_report_anyonmous_user(self):
        
        response = self.client.get(reverse('Report'))
        self.assertEqual(response.status_code, 302)

class TestLaundererOngoingOrderView(TestSetup):

    def test_should_show_ongoin_order_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ongoingOrders"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_ongoin_order_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ongoingOrders"), follow=True)

        self.assertTemplateUsed(response2, "frontend/ongoingOrders.html")

    def test_should_not_show_ongoing_order_anyonmous_user(self):
        
        response = self.client.get(reverse('ongoingOrders'))
        self.assertEqual(response.status_code, 302)

class TestLaundererOrderHistoryView(TestSetup):

    def test_should_show_order_history_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ordersHistory"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_order_history_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ordersHistory"), follow=True)

        self.assertTemplateUsed(response2, "frontend/ordersHistory.html")

    def test_should_not_show_order_history_anyonmous_user(self):
        
        response = self.client.get(reverse('ordersHistory'))
        self.assertEqual(response.status_code, 302)

class TestLaundererOrderRequestView(TestSetup):

    def test_should_show_order_reuqest_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ordersRequest"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_order_requet_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("ordersRequest"), follow=True)

        self.assertTemplateUsed(response2, "frontend/orderRequests.html")

    def test_should_not_show_order_request_anyonmous_user(self):
        
        response = self.client.get(reverse('ordersRequest'))
        self.assertEqual(response.status_code, 302)

class TestLaundererOrderRequestProcessView(TestSetup):

    def test_should_accept_launderer_order(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_pending(client, launderette, services)
        data = {
            'statusField': 'accept'
        }
        response2 = self.client.post(reverse("orderRequestProcess", kwargs={'pk_id': order.id}), data , follow=True)
        orders = Order.objects.all()
        order = orders[0]

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEquals(response2.redirect_chain[0][0], '/dashboard/orders/requests/')
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(order.status, 'ongoing')
    
    def test_should_decline_launderer_order(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_pending(client, launderette, services)
        data = {
            'statusField': 'declined'
        }
        response2 = self.client.post(reverse("orderRequestProcess", kwargs={'pk_id': order.id}), data , follow=True)
        orders = Order.objects.all()
        order = orders[0]

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEquals(response2.redirect_chain[0][0], '/dashboard/orders/requests/')
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(order.status, 'declined')

class TestLaundererOrderDetailView(TestSetup):

    def test_should_show_launderer_order_detail(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_ongoing(client, launderette, services)
        
        response2 = self.client.get(reverse("orderDetail", kwargs={'pk_id': order.id}) , follow=True)
        
        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(order.status, 'ongoing')
      
    def test_should_check_launderer_order_detail_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_ongoing(client, launderette, services)
        
        response2 = self.client.get(reverse("orderDetail", kwargs={'pk_id': order.id}) , follow=True)

        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'frontend/orderDetail.html')
              
    def test_should_change_order_to_finished_from_launderer_order_detail(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_ongoing(client, launderette, services)
        
        data = {
            'statusField': 'finished'
        }

        response2 = self.client.post(reverse("orderDetail", kwargs={'pk_id': order.id}), data , follow=True)
        orders = Order.objects.all()
        order = orders[0]

        self.assertEquals(response2.redirect_chain[0][0], '/dashboard/orders/ongoing/')
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(order.status, 'finished')
                  
    def test_should_change_order_to_cancel_from_launderer_order_detail(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        Services.objects.create(
            launderette = launderette,
            title = "test service 2",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_ongoing(client, launderette, services)
        
        data = {
            'statusField': 'cancel'
        }

        response2 = self.client.post(reverse("orderDetail", kwargs={'pk_id': order.id}), data , follow=True)
        orders = Order.objects.all()
        order = orders[0]

        self.assertEquals(response2.redirect_chain[0][0], '/dashboard/orders/ongoing/')
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(order.status, 'cancel')

class TestLaundererServicesView(TestSetup):

    def test_should_show_services_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("services"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_service_anyonmous_user(self):
        
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 302)

class TestLaundererServiceEditView(TestSetup):

    def test_should_show_services_edit_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        response2 = self.client.get(reverse("editServices", kwargs={'pk_id': service.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_services_edit_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        response2 = self.client.get(reverse("editServices", kwargs={'pk_id': service.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/servicesEdit.html")

    def test_should_update_services(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        response2 = self.client.get(reverse("editServices", kwargs={'pk_id': service.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/servicesEdit.html")
        pretitle = service.title
        service.title = 'service'
        service.save()
        form  = ServicesForm(instance=service)
        data = {
             'launderer' : launderer, 
             'title': 'service'
        }
        
        response3 = self.client.post(reverse("editServices", kwargs={'pk_id': service.id}), data, follow=True)
        
        posttitle = Services.objects.all()[0].title
        
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/servicesEdit.html")
        self.assertFalse(pretitle==posttitle)

        
    def test_should_not_update_services(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        response2 = self.client.get(reverse("editServices", kwargs={'pk_id': service.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/servicesEdit.html")
        pretitle = service.title
        service.title = 'service'
        data = {
             'launderer' : launderer, 
             'title': 'service'
        }
        
        response3 = self.client.post(reverse("editServices", kwargs={'pk_id': service.id}), data, follow=True)
        
        posttitle = Services.objects.all()[0].title
        
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/servicesEdit.html")
        self.assertTrue(pretitle==posttitle)
        
class TestLaundererServiceDeleteView(TestSetup):

    def test_should_delete_service(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        response2 = self.client.post(reverse("deleteServices", kwargs={'pk_id': service.id}))
        services = Services.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(services, 0)

class TestLaundererServiceNewView(TestSetup):

    def test_should_create_service(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        data = {
            'launderette': launderette,
            'title': "test service",
            'price': 10
        }
        response2 = self.client.post(reverse("newService"),data)
        services = Services.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(services, 1)


    def test_should_not_create_service(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        self.create_test_launderette(launderer)
        data = {
        }
        response2 = self.client.post(reverse("newService"),data)
        services = Services.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(services==1)

    def test_should_not_show_new_service_anyonmous_user(self):
        
        response = self.client.get(reverse('newService'))
        self.assertEqual(response.status_code, 302)

class TestLaundererComplaintView(TestSetup):

    def test_should_show_complaints_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("complaints"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_complaints_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("complaints"), follow=True)

        self.assertTemplateUsed(response2, "frontend/complaints.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_complaints_anyonmous_user(self):
        
        response = self.client.get(reverse('complaints'))
        self.assertEqual(response.status_code, 302)

class TestLaundererComplaintDetailView(TestSetup):

    def test_should_show_complaint_detail_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        complaint = self.create_test_launderer_complaint()
        complaint.launderer = launderer
        complaint.save()

        response2 = self.client.get(reverse("complaintDetail", kwargs={'pk_id': complaint.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_complaint_detail_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        complaint = self.create_test_launderer_complaint()
        complaint.launderer = launderer
        complaint.save()

        response2 = self.client.get(reverse("complaintDetail", kwargs={'pk_id': complaint.id}), follow=True)

        self.assertTemplateUsed(response2, "frontend/complaintDetail.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_complaint_detail_anyonmous_user(self):
        complaint = self.create_test_launderer_complaint()

        response = self.client.get(reverse('complaintDetail', kwargs={'pk_id': complaint.id}))
        self.assertEqual(response.status_code, 302)

class TestLaundererComplaintNewView(TestSetup):

    def test_should_show_complaint_new_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("newComplaint"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_create_complaint(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        launderette = self.create_test_launderette(launderer)
        data = {
            'subject': "test complaint",
            'complain': 'test complaint test complaint',
        }
        form = ComplaintForm(data=data)
        data = {
            'launderer': launderer,
            'user': launderer.user,
            'complaintForm': form,
            'subject': "test complaint",
            'complain': 'test complaint test complaint'
        }
        response2 = self.client.post(reverse("newComplaint"),data, follow=True)
        complaints = Complaint.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(complaints, 0)

    def test_should_not_create_complaint(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        self.create_test_launderette(launderer)
        data = {
        }
        response2 = self.client.post(reverse("newComplaint"),data)
        complaints = Complaint.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertFalse(complaints==1)

    def test_should_not_show_new_complaint_anyonmous_user(self):
        
        response = self.client.get(reverse('newComplaint'))
        self.assertEqual(response.status_code, 302)

    def test_should_check_complaint_detail_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("newComplaint"), follow=True)

        self.assertTemplateUsed(response2, "frontend/complaintNew.html")
        self.assertEqual(response2.status_code, 200)

class TestLaundererLaundereteView(TestSetup):

    def test_should_show_launderette_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        self.create_test_launderette(launderer)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("launderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_launderette_page_template(self):
        
        launderer = self.create_test_launderer()
        self.create_test_launderette(launderer)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("launderette"), follow=True)

        self.assertTemplateUsed(response2, "frontend/launderette.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_launderette_anyonmous_user(self):
        
        response = self.client.get(reverse('launderette'))
        self.assertEqual(response.status_code, 302)


    def test_should_redirect_from_new_launderette_page(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("launderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/newLaunderette.html")

class TestLaundererLaundereteEditView(TestSetup):

    def test_should_show_launderette_edit_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("editlaunderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_launderette_edit_template(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("editlaunderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/launderetteEdit.html")

    def test_should_update_launderette(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("editlaunderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/launderetteEdit.html")
        pretitle = launderette.name
        launderette.name = 'new name'
        launderette.save()
        data = {
             'launderer' : launderer, 
             'name': 'launderette'
        }
        
        response3 = self.client.post(reverse("editlaunderette"), data, follow=True)
        
        posttitle = Launderette.objects.all()[0].name
        
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/launderetteEdit.html")
        self.assertFalse(pretitle==posttitle)

        
    def test_should_not_update_launderette(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("editlaunderette"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/launderetteEdit.html")
        pretitle = launderette.name
        launderette.name = 'new name'
        data = {
        }
        
        response3 = self.client.post(reverse("editlaunderette"), data, follow=True)
        
        posttitle = Launderette.objects.all()[0].name
        
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/launderetteEdit.html")
        self.assertTrue(pretitle==posttitle)
        
class TestLaundererLaundereteReviewView(TestSetup):

    def test_should_show_launderette_review_page_to_launderer(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("laundaretteReviews"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_launderette_review_page_template(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("laundaretteReviews"), follow=True)

        self.assertTemplateUsed(response2, "frontend/launderetteReviews.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_launderette_review_anyonmous_user(self):
        
        response = self.client.get(reverse('laundaretteReviews'))
        self.assertEqual(response.status_code, 302)

    def test_should_redirect_from_launderette_page(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("laundaretteReviews"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "frontend/newLaunderette.html")
      
class TestLaundererLaundereteReviewDetailView(TestSetup):

    def test_should_show_launderette_review_detail_page_to_launderer(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("laundaretteReviewDetail", kwargs={'pk_id': review.id}), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_launderette_review_detail_page_template(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("laundaretteReviewDetail", kwargs={'pk_id': review.id}), follow=True)

        self.assertTemplateUsed(response2, "frontend/launderetteReviewDetail.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_add_comment_from_launderette_review_detail_page(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        data = {
            'comment': 'comment',
            'review': review,
            'launderette': launderette
        }

        response2 = self.client.post(reverse("laundaretteReviewDetail", kwargs={'pk_id': review.id}), data, follow=True)

        reviewComment = ReviewComment.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertFalse(reviewComment==0)


    def test_should_not_add_comment_from_launderette_review_detail_page(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        data = {
        }

        response2 = self.client.post(reverse("laundaretteReviewDetail", kwargs={'pk_id': review.id}), data, follow=True)

        reviewComment = ReviewComment.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(reviewComment==0)
        
class TestLaundererLaundereteReviewDetailDeleteView(TestSetup):

    def test_should_delete_review_comment(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        reviewwComment = ReviewComment.objects.create(
            comment = 'comment',
            review = review,
            launderette = launderette
        )

        response2 = self.client.post(reverse("deleteComment", kwargs={'pk_id': reviewwComment.id}), follow=True)

        reviewComments = ReviewComment.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(reviewComments, 0)

    def test_should_not_delete_review_comment(self):
        
        client = self.create_test_client()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client,launderette,services)
        review = self.create_test_review_bad(client,launderette, order)
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        reviewwComment = ReviewComment.objects.create(
            comment = 'comment',
            review = review,
            launderette = launderette
        )

        response2 = self.client.get(reverse("deleteComment", kwargs={'pk_id': reviewwComment.id}), follow=True)

        reviewComments = ReviewComment.objects.all().count()

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(reviewComments, 1)

class TestLaundererProfileView(TestSetup):

    def test_should_show_launderer_profile_page_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("myAccount"), follow=True)

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)

    def test_should_check_launderer_profile_page_template(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse("myAccount"), follow=True)

        self.assertTemplateUsed(response2, "frontend/profile.html")
        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_launderer_profile_anyonmous_user(self):
        
        response = self.client.get(reverse('myAccount'))
        self.assertEqual(response.status_code, 302)

class TestLaundererChangeGenralInfoView(TestSetup):

    def test_should_not_change_launderer_general_info(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)
        prename = launderer.name

        data = {
        }
        response2 = self.client.post(reverse("generalInfo"), data, follow=True)

        postname = ""

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertFalse(prename==postname)

    def test_should_change_launderer_general_info(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)
        prename = launderer.name

        data = {
             'name': 'launderer change'
        }
        response2 = self.client.post(reverse("generalInfo"), data, follow=True)

        postname = Launderer.objects.all()[0].name

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(prename==postname)

class TestAdminLoginView(TestSetup):

    def test_should_show_admin_login_page(self):
        response = self.client.get(reverse('adminLoginPage'))
        self.assertEqual(response.status_code, 200)

    def test_should_check_admin_login_page_template(self):
        response = self.client.get(reverse('adminLoginPage'))
        self.assertTemplateUsed(response, "frontend/admin/login.html")

    def test_should_login_admin_successfully(self):
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        })

        self.assertEquals(response.status_code, 302)

    def test_should_not_login_launderer(self):
        launderer = self.create_test_launderer()
        user = launderer.user
        Group.objects.create(name='launderer')
        my_group= Group.objects.get(name='launderer')
        my_group.user_set.add(user)
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        })
        self.assertEquals(response.status_code, 409)

class TestAdminDashboardView(TestSetup):

    def test_should_show_dashboard_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(response.redirect_chain[0][0], follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_dashboard_anyonmous_user(self):
        
        response = self.client.get(reverse('adminDashboard'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_dashboard_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminDashboard'))
        self.assertEqual(response.status_code, 302)

class TestAdminLaundererView(TestSetup):

    def test_should_show_launderer_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(response.redirect_chain[0][0], follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_launderer_anyonmous_user(self):
        
        response = self.client.get(reverse('adminLaunderers'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_launderer_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminLaunderers'))
        self.assertEqual(response.status_code, 302)

class TestAdminLaundererDetailView(TestSetup):

    def test_should_show_launderer_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        launderer = self.create_test_launderer()
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminLaundererDetail', kwargs={'pk_id':launderer.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_launderer_detail_anyonmous_user(self):
        
        launderer = self.create_test_launderer()
        response = self.client.get(reverse('adminLaundererDetail', kwargs={'pk_id':launderer.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_launderer_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminLaundererDetail', kwargs={'pk_id':launderer.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminLaunderetteView(TestSetup):

    def test_should_show_launderette_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(response.redirect_chain[0][0], follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_launderette_anyonmous_user(self):
        
        response = self.client.get(reverse('adminLaunderettes'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_launderette_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminLaunderettes'))
        self.assertEqual(response.status_code, 302)

class TestAdminLaunderetteDetailView(TestSetup):

    def test_should_show_launderette_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminLaunderetteDetail', kwargs={'pk_id':launderette.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_launderette_detail_anyonmous_user(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        response = self.client.get(reverse('adminLaunderetteDetail', kwargs={'pk_id':launderette.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_launderette_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        launderette = self.create_test_launderette(launderer)

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminLaunderetteDetail', kwargs={'pk_id':launderette.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminClientView(TestSetup):

    def test_should_show_client_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminClients'), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_client_anyonmous_user(self):
        
        response = self.client.get(reverse('adminClients'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_client_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminClients'))
        self.assertEqual(response.status_code, 302)

class TestAdminClientDetailView(TestSetup):

    def test_should_show_client_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        client = self.create_test_client()
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminClientDetail', kwargs={'pk_id':client.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_client_detail_anyonmous_user(self):
        
        client = self.create_test_client()
        response = self.client.get(reverse('adminClientDetail', kwargs={'pk_id':client.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_client_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        client = self.create_test_client()

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminClientDetail', kwargs={'pk_id':client.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminReviewView(TestSetup):

    def test_should_show_review_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminReviews'), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_review_anyonmous_user(self):
        
        response = self.client.get(reverse('adminReviews'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_review_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminReviews'))
        self.assertEqual(response.status_code, 302)

class TestAdminReviewDetailView(TestSetup):

    def test_should_show_review_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)
        review = self.create_test_review_good(client, launderette, order)
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminReviewDetail', kwargs={'pk_id':review.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_review_detail_anyonmous_user(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)
        review = self.create_test_review_good(client, launderette, order)
        response = self.client.get(reverse('adminReviewDetail', kwargs={'pk_id':review.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_review_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)
        review = self.create_test_review_good(client, launderette, order)

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminReviewDetail', kwargs={'pk_id':review.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminOrderView(TestSetup):

    def test_should_show_order_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminOrders'), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_order_anyonmous_user(self):
        
        response = self.client.get(reverse('adminOrders'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_order_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminOrders'))
        self.assertEqual(response.status_code, 302)

class TestAdminOrderDetailView(TestSetup):

    def test_should_show_order_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminOrderDetails', kwargs={'pk_id':order.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_order_review_detail_anyonmous_user(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)
        response = self.client.get(reverse('adminOrderDetails', kwargs={'pk_id':order.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_order_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        launderette = self.create_test_launderette(launderer)
        client = self.create_test_client()
        Services.objects.create(
            launderette = launderette,
            title = "tesst sservice",
            price = 10
        )
        services = Services.objects.all()
        order = self.create_test_order_finished(client, launderette, services)

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminOrderDetails', kwargs={'pk_id':order.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminAnalyticView(TestSetup):

    def test_should_show_analytic_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('AdminReports'), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_analytic_anyonmous_user(self):
        
        response = self.client.get(reverse('AdminReports'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_analytic_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('AdminReports'))
        self.assertEqual(response.status_code, 302)

class TestAdminAnalyticLaunderetteView(TestSetup):

    def test_should_show_analytic_launderette_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('AdminLaunderetePerfomance', kwargs={'pk_id':launderette.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_analytic_launderette_anyonmous_user(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        
        response = self.client.get(reverse('AdminLaunderetePerfomance', kwargs={'pk_id':launderette.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_analytic_launderette_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        launderette = self.create_test_launderette(launderer)

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('AdminLaunderetePerfomance', kwargs={'pk_id':launderette.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminComplaintsView(TestSetup):

    def test_should_show_complaints_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminComplaints'), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)

    def test_should_not_show_admin_complaints_anyonmous_user(self):
        
        response = self.client.get(reverse('adminComplaints'))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_admin_complaints_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminComplaints'))
        self.assertEqual(response.status_code, 302)

class TestAdminComplaintDetailView(TestSetup):

    def test_should_show_complaint_detail_page_to_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        complaint = self.create_test_launderer_complaint()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response2 = self.client.get(reverse('adminComplaintsDetail', kwargs={'pk_id':complaint.id}), follow=True)
        self.assertEquals(response.redirect_chain[0][1], 302)

        self.assertEqual(response2.status_code, 200)


    def test_should_resolve_complaint_by_admin(self):
        
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        complaint = self.create_test_launderer_complaint()
        
        response = self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)
        
        form = ComplaintForm(instance= complaint)
        data = {
            'response': "my test response",
            'form': form,
            'complaint': complaint
        }
        preStatus = complaint.status

        response2 = self.client.post(reverse('adminComplaintsDetail', kwargs={'pk_id':complaint.id}), data, follow=True)
        complaint.status = 'resolved';
        complaint.save()
        
        postStatus = Complaint.objects.all()[0].status

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(postStatus, 'resolved')
        self.assertFalse(preStatus==postStatus)


    def test_should_not_show_complaint_review_detail_anyonmous_user(self):
        
        complaint = self.create_test_launderer_complaint()

        response = self.client.get(reverse('adminComplaintsDetail', kwargs={'pk_id':complaint.id}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_complaint_order_detail_to_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.is_email_verified = True
        launderer.save()
        user = launderer.user
        
        complaint = self.create_test_launderer_complaint()

        self.client.post(reverse("adminLoginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        response = self.client.get(reverse('adminComplaintsDetail', kwargs={'pk_id':complaint.id}))
        self.assertEqual(response.status_code, 302)

class TestAdminClientRequestProcess(TestSetup):

    def test_should_block_client(self):
        
        client = self.create_test_client()
        client.isBlocked = False
        client.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = client.isBlocked
        client.isBlocked = True
        client.save()
        
        data = {
            'statusField': 'block'
        }

        response2 = self.client.post(reverse("clientRequestProcess", kwargs={'pk_id': client.id}), {
            'statusField': 'block'
        } , follow=True)

        clients = Client.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(clients, True)
        self.assertFalse(prestatus==clients)
 
    def test_should_not_block_client(self):
        
        client = self.create_test_client()
        client.isBlocked = False
        client.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = client.isBlocked
        

        response2 = self.client.get(reverse("clientRequestProcess", kwargs={'pk_id': client.id}), follow=True)

        clients = Client.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(clients, prestatus)
        self.assertTrue(prestatus==clients)
       
    def test_should_unblock_client(self):
        
        client = self.create_test_client()
        client.isBlocked = True
        client.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = client.isBlocked
        client.isBlocked = False
        client.save()
        
        data = {
            'statusField': 'unblock'
        }

        response2 = self.client.post(reverse("clientRequestProcess", kwargs={'pk_id': client.id}), data , follow=True)

        clients = Client.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(clients, False)
        self.assertFalse(prestatus==clients)
 

class TestAdminLaundererRequestProcess(TestSetup):

    def test_should_block_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.isBlocked = False
        launderer.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderer.isBlocked
        launderer.isBlocked = True
        launderer.save()
        
        data = {
            'statusField': 'block'
        }

        response2 = self.client.post(reverse("laundererRequestProcess", kwargs={'pk_id': launderer.id}), {
            'statusField': 'block'
        } , follow=True)

        launderers = Launderer.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderers, True)
        self.assertFalse(prestatus==launderers)
 
    def test_should_not_block_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.isBlocked = False
        launderer.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderer.isBlocked
        
        response2 = self.client.get(reverse("laundererRequestProcess", kwargs={'pk_id': launderer.id}), follow=True)

        launderers = Launderer.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderers, prestatus)
        self.assertTrue(prestatus==launderers)
       
    def test_should_unblock_launderer(self):
        
        launderer = self.create_test_launderer()
        launderer.isBlocked = True
        launderer.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderer.isBlocked
        launderer.isBlocked = False
        launderer.save()
        
        data = {
            'statusField': 'unblock'
        }

        response2 = self.client.post(reverse("laundererRequestProcess", kwargs={'pk_id': launderer.id}), data , follow=True)

        launderers = Launderer.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderers, False)
        self.assertFalse(prestatus==launderers)
 

class TestAdminLaunderetteRequestProcess(TestSetup):

    def test_should_block_launderette(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderette.isBlocked = False
        launderette.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderette.isBlocked
        launderette.isBlocked =True
        launderette.save()

        data = {
            'statusField': 'block'
        }

        response2 = self.client.post(reverse("launderetteRequestProcess", kwargs={'pk_id': launderette.id}), {
            'statusField': 'block'
        } , follow=True)

        launderettes = Launderette.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderettes, True)
        self.assertFalse(prestatus==launderettes)
 
    def test_should_not_block_launderette(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderette.isBlocked = False
        launderette.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderer.isBlocked
        
        
        response2 = self.client.get(reverse("launderetteRequestProcess", kwargs={'pk_id': launderette.id}), follow=True)

        launderettes = Launderette.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderettes, prestatus)
        self.assertTrue(prestatus==launderettes)
       
    def test_should_unblock_launderette(self):
        
        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderette.isBlocked = True
        launderette.save()
        user = self.create_test_user()
        user.is_staff = True
        user.save()
        response = self.client.post(reverse("loginPage"), {
            'username': user.username,
            'password': 'password12!'
        }, follow=True)

        prestatus = launderette.isBlocked
        launderette.isBlocked = False
        launderette.save()
        
        data = {
            'statusField': 'unblock'
        }

        response2 = self.client.post(reverse("launderetteRequestProcess", kwargs={'pk_id': launderette.id}), data , follow=True)

        launderettes = Launderette.objects.all()[0].isBlocked

        self.assertEquals(response.redirect_chain[0][1], 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEquals(launderettes, False)
        self.assertFalse(prestatus==launderettes)
 




