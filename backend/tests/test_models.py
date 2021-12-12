from utils.setup_test import TestSetup
from backend.models import Order, Client, Launderer, Launderette, Complaint, Services, Review, ReviewComment


class TestUserModel(TestSetup):

    def test_should_create_user(self):

        user = self.create_test_user()

        self.assertEqual(str(user), user.username)
        
class TestClientModel(TestSetup):

    def test_should_create_client(self):

        client = self.create_test_client()
        clients = Client.objects.all()

        self.assertEqual(clients.count(), 1)
        self.assertEqual(str(client), client.user.username)

class TestLaundererModel(TestSetup):

    def test_should_create_launderer(self):

        launderers = Launderer.objects.all()
        
        launderer = self.create_test_launderer()
        launderers = Launderer.objects.all()

        self.assertEqual(launderers.count(), 1)
        self.assertEqual(str(launderer), launderer.user.username)
        
class TestLaunderetteModel(TestSetup):

    def test_should_create_launderette(self):

        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        launderettes = Launderette.objects.all()

        self.assertEqual(launderettes.count(), 1)
        self.assertEqual(str(launderette.launderer), launderer.user.username)
       
class TestComplaintModel(TestSetup):

    def test_should_create_complaint(self):

        complaint = self.create_test_launderer_complaint()
        complaints = Complaint.objects.all().count()

        self.assertEqual(complaints, 1)
        self.assertEqual(complaint.launderer, None)
        self.assertEqual(complaint.client, None)     
    
    def test_should_create_launderer_complaint(self):

        launderer = self.create_test_launderer()
        complaint = self.create_test_launderer_complaint()
        complaint.launderer = launderer;
        complaint.save()
        complaints = Complaint.objects.all().count()

        self.assertEqual(complaints, 1)
        self.assertEqual(str(complaint.launderer), launderer.user.username)
        self.assertEqual(complaint.client, None)
    
    def test_should_create_client_complaint(self):

        client = self.create_test_client()
        complaint = self.create_test_launderer_complaint()
        complaint.client = client;
        complaint.save()
        complaints = Complaint.objects.all().count()

        self.assertEqual(complaints, 1)
        self.assertEqual(str(complaint.client), client.user.username)
        self.assertEqual(complaint.launderer, None)

class TestServiceModel(TestSetup):

    def test_should_create_launderette_service(self):

        launderer = self.create_test_launderer()
        launderette = self.create_test_launderette(launderer)
        service = Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        self.assertEqual(services.count(), 1)
        self.assertEqual(service.launderette, launderette)

class TestOrderModel(TestSetup):

    def test_should_create_client_pending_order_single_service(self):

        launderer = self.create_test_launderer()
        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        order = self.create_test_order_pending(client, launderette, services)
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)

    def test_should_create_client_ongoing_order_single_service(self):

        launderer = self.create_test_launderer()
        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        order = self.create_test_order_ongoing(client, launderette, services)
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)
        
    def test_should_create_client_finished_order_single_service(self):

        launderer = self.create_test_launderer()
        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        order = self.create_test_order_finished(client, launderette, services)
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)
        
    def test_should_create_client_pending_order_multi_service(self):

        launderer = self.create_test_launderer()
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
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)

        
    def test_should_create_client_ongoing_order_multi_service(self):

        launderer = self.create_test_launderer()
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
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)

    def test_should_create_client_finished_order_multi_service(self):

        launderer = self.create_test_launderer()
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

        order = self.create_test_order_finished(client, launderette, services)
        orders = Order.objects.all().count()

        self.assertEqual(orders, 1)
        self.assertEqual(order.launderette, launderette)
        self.assertEqual(order.client, client)

class TestReviewModel(TestSetup):

    def test_should_create_good_review(self):
        launderer = self.create_test_launderer()
        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        order = self.create_test_order_finished(client, launderette, services)

        review = self.create_test_review_good(client, launderette, order)

        reviews = Review.objects.all().count()

        self.assertEqual(reviews, 1)
        self.assertEqual(review.launderette, launderette)
        self.assertEqual(review.client, client)
        self.assertEqual(review.order, order)

    def test_should_create_client_finished_order_multi_service_bad_review(self):

        launderer = self.create_test_launderer()
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

        order = self.create_test_order_finished(client, launderette, services)

        review = self.create_test_review_bad(client, launderette, order)

        reviews = Review.objects.all().count()

        self.assertEqual(reviews, 1)
        self.assertEqual(review.launderette, launderette)
        self.assertEqual(review.client, client)
        self.assertEqual(review.order, order)
        
class TestReviewCommentModel(TestSetup):

    def test_should_create_comment_on_review(self):
        launderer = self.create_test_launderer()
        client = self.create_test_client()
        launderette = self.create_test_launderette(launderer)
        Services.objects.create(
            launderette = launderette,
            title = "test service",
            price = 10
        )
        services = Services.objects.all()

        order = self.create_test_order_finished(client, launderette, services)

        review = self.create_test_review_good(client, launderette, order)

        review_comment = self.create_test_review_comment(client, launderette, review)
        
        review_comments = ReviewComment.objects.all().count()

        self.assertEqual(review_comments, 1)
        self.assertEqual(review_comment.launderette, review.launderette)
        self.assertEqual(review_comment.client, review.client)
        self.assertEqual(review_comment.review, review)
