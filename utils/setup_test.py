from django.test import TestCase
from backend.models import User, Complaint, Launderer, Launderette, Client, Review, Order, ReviewComment
from faker import Faker


class TestSetup(TestCase):

    def setUp(self):

        self.faker = Faker()
        self.password = self.faker.paragraph(nb_sentences=3)

        self.user = {
            "username": self.faker.name().split(" ")[0],
            "email": self.faker.email(),
            "password": self.password,
            "password2": self.password
        }

    def create_test_user(self):
        user = User.objects.create_user(
            username='username', email='email@app.com')
        user.set_password('password12!')
        user.save()
        return user

    def create_test_client(self):
        user = User.objects.create_user(
            username='client1', email='emailclient1@app.com')
        user.set_password('password12!')
        user.save()
        client = Client.objects.create(
               user=user,
               name="test client 1",
               city="city",
               address="addres",
               lat= 90,
               lon = 120,
            )
        return client

    def create_test_launderer(self):
        user = User.objects.create_user(
            username='launderer1', email='emaillaunderer1@app.com')
        user.set_password('password12!')
        user.save()
        launderer = Launderer.objects.create(
               user=user,
               name="test launderer 1",
               city="city",
               address="addres",
               lat= 90,
               lon = 120,
            )
        return launderer

    def create_test_launderette(self, launderer):
        launderette = Launderette.objects.create(
               launderer = launderer,
               name = "name",
               available_time = "available_time",
               location = "location",
               delivery_fee_pkm = 10,
            )
        return launderette
        
    def create_test_launderer2(self, launderer):
        launderette = Launderette.objects.create(
               launderer = launderer,
               name = "name2",
               available_time = "available_time2",
               location = "location2",
               delivery_fee_pkm = 12,
            )
        return launderette

    def create_test_user_two(self):
        user = User.objects.create_user(
            username='username2', email='email2@app.com')
        user.set_password('password12!')
        user.save()
        return user

    def create_test_launderer_complaint(self):
        complaint = Complaint.objects.create(
               subject = "subject",
               complain = self.faker.paragraph(nb_sentences=5),
            )
        return complaint

    def create_test_order_pending(self, client, launderette, services):
        order = Order.objects.create(
            client =client,
            launderette = launderette,
            status = "pending",
            description = self.faker.paragraph(nb_sentences=5),
        )
        order.services.set(services)
        order.save()
        return order

    def create_test_order_ongoing(self, client, launderette, services):
        order = Order.objects.create(
            client =client,
            launderette = launderette,
            status = "ongoing",
            description = self.faker.paragraph(nb_sentences=5),
        )
        order.services.set(services)
        order.save()
        return order

    def create_test_order_finished(self, client, launderette, services):
        order = Order.objects.create(
            client =client,
            launderette = launderette,
            status = "finished",
            description = self.faker.paragraph(nb_sentences=5),
        )
        order.services.set(services)
        order.save()
        return order

    def create_test_review_good(self, client, launderette, order):
        review = Review.objects.create(
            client =client,
            launderette = launderette,
            order = order,
            rating = 5,
            review = self.faker.paragraph(nb_sentences=5),
        )
        return review

    def create_test_review_bad(self, client, launderette, order):
        review = Review.objects.create(
            client =client,
            launderette = launderette,
            order = order,
            rating = 1,
            review = self.faker.paragraph(nb_sentences=5),
        )
        return review

    def create_test_review_comment(self, client, launderette, review):
        review_comment = ReviewComment.objects.create(
            client =client,
            launderette = launderette,
            review = review,
            comment = self.faker.paragraph(nb_sentences=5),
        )
        return review_comment

    def tearDown(self):
        return super().tearDown()