
from django.db.models import fields
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from backend.models import *

class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class CLUserSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(
    #     queryset = User.objects.all(),
    #     view_name = 'user-details'
    # )

    class Meta:
        model = User
        fields = '__all__'    

class LaundererSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(
    #     queryset = User.objects.all(),
    #     view_name = 'user-details'
    # )

    class Meta:
        model = Launderer
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # subject = serializers.CharField()
    # complain = serializers.CharField()
    # status = serializers.CharField()
    # date = serializers.DateTimeField()
    # client = serializers.StringRelatedField()
    # # launderer = LaundererSerializer()
    
    # launderer = serializers.HyperlinkedRelatedField(
    #     queryset = Launderer.objects.all(),
    #     view_name = 'launderer-details'
    # )
    
    class Meta:
        model = Complaint
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'

class LaunderetteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Launderette
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Services
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReviewComment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
