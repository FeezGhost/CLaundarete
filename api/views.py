# from django.db.models import query
# from django.http import request
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.mixins import ListModelMixin
# from rest_framework.views import APIView
# from rest_framework import mixins
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from re import search
from django_filters import filters, filterset
from rest_framework.viewsets import ModelViewSet
# from rest_framework import status
from backend.models import *
from .serializers import *
from backend.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsCreatorOrIsAdmin, IsCreatorLaunderetteOrIsAdmin

class ComplaintViewSet(ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    permission_classes = [IsCreatorOrIsAdmin]

    filter_backends = [DjangoFilterBackend, SearchFilter,  OrderingFilter]
    filterset_class = ComplaintFilter

    search_fields = ['subject', 'complain', 'response']

    ordering_fields=  ['date']

    def get_serializer_context(self):
        return {'request': self.request}

class LaundererViewSet(ModelViewSet):
    
    permission_classes = [IsCreatorOrIsAdmin]

    queryset = Launderer.objects.all()
    serializer_class = LaundererSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LaundererFilter


    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (launderer, created) = Launderer.objects.get_or_create(user__id=request.user.id)
        if request.method == "GET":
            serializer = LaundererSerializer(launderer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = LaundererSerializer(launderer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}
       
class UserViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrIsAdmin]

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CLUserViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrIsAdmin]

    queryset = User.objects.all()
    serializer_class = CLUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ClientViewSet(ModelViewSet):

    queryset = Client.objects.all()
    permission_classes = (IsCreatorOrIsAdmin, )
    serializer_class = ClientSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter


    def get_serializer_context(self):
        return {'request': self.request}

class LaunderetteViewSet(ModelViewSet):
    queryset = Launderette.objects.all()
    serializer_class = LaunderetteSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LaunderetteFilter

    permission_classes = [IsCreatorOrIsAdmin]
    
    def get_serializer_context(self):
        return {'request': self.request,}

class LaundererLaunderetteViewSet(ModelViewSet):
    queryset = Launderette.objects.all()
    serializer_class = LaunderetteSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LaunderetteFilter

    permission_classes = [IsCreatorOrIsAdmin]

    def get_queryset(self):
        return Launderette.objects.filter(launderer_id=self.kwargs['launderer_pk'])

    def get_serializer_context(self):
        return {'request': self.request,}

class ServicesViewSet(ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

    permission_classes = [IsCreatorLaunderetteOrIsAdmin]

    def get_serializer_context(self):
        return {'request': self.request}

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    permission_classes = [IsCreatorLaunderetteOrIsAdmin]

    def get_serializer_context(self):
        return {'request': self.request}

class ReviewCommentViewSet(ModelViewSet):
    queryset = ReviewComment.objects.all()
    serializer_class = ReviewCommentSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [IsCreatorLaunderetteOrIsAdmin]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_serializer_context(self):
        return {'request': self.request}



