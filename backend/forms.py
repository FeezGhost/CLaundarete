from django.forms import ModelForm, fields
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class CreatUserForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Full Name.', label='Full Name')
    class Meta:
        model =  User
        fields =  ['username', 'name', 'email','password1', 'password2']

class ServicesForm(ModelForm):
    # des=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10, "style": "resize: none"}))
    # e_date=forms.DateField(widget=DateInput, required=False)
    
    class Meta:
        model = Services
        fields = '__all__'
        exclude = ['launderette']


class LaundererForm(ModelForm):
    
    class Meta:
        model = Launderer
        fields = '__all__'
        exclude = ['user']


class LaunderetteForm(ModelForm):
    
    class Meta:
        model = Launderette
        fields = '__all__'
        exclude = ['launderer']

class ReviewCommentForm(ModelForm):
    comment=forms.CharField(widget=forms.Textarea(attrs={"rows":5,  }))
    
    class Meta:
        model = ReviewComment
        exclude = '__all__'
        fields = ['comment']

class LaundererProfilePicForm(ModelForm):
    
    class Meta:
        model = Launderer
        fields = ['profile_pic']


class LaundererEmailForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['email']

class ComplaintForm(ModelForm):
    complain=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))
    response=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))

    class Meta:
        model = Complaint
        fields = "__all__"