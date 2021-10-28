from django.urls import path
from django.urls.conf import include
from . import views
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('complaints', views.ComplaintViewSet)
router.register('launderers', views.LaundererViewSet)
router.register('clients', views.ClientViewSet)
router.register('users', views.CLUserViewSet)
router.register('launderettes', views.LaunderetteViewSet)
router.register('services', views.ServicesViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('review-comments', views.ReviewCommentViewSet)
router.register('orders', views.OrderViewSet)

launderette_router = routers.NestedDefaultRouter(router, 'launderettes', lookup='launderette')
launderette_router.register('reviews', views.ReviewViewSet, basename="launderette-reviews")
launderette_router.register('services', views.ServicesViewSet, basename="launderette-services")
launderette_router.register('orders', views.OrderViewSet, basename="launderette-orders")

client_router = routers.NestedDefaultRouter(router, 'clients', lookup='client')
client_router.register('reviews', views.ReviewViewSet, basename="client-reviews")
client_router.register('orders', views.OrderViewSet, basename="client-orders")
client_router.register('complaints', views.ComplaintViewSet, basename="client-complaints")

launderer_router = routers.NestedDefaultRouter(router, 'launderers', lookup='launderer')
launderer_router.register('launderettes', views.LaundererLaunderetteViewSet, basename="launderer-launderettes")
launderer_router.register('complaints', views.ComplaintViewSet, basename="launderer-complaints")

review_router = routers.NestedDefaultRouter(router, 'reviews', lookup='review')
review_router.register('review-comments', views.ReviewCommentViewSet, basename="review-reviewcomments")

# urlpatterns = router.urls + launderette_router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(launderette_router.urls)),
    path('', include(client_router.urls)),
    path('', include(launderer_router.urls)),
    path('', include(review_router.urls)),
]
