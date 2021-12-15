from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type = 'date'

class CreatUserForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Full Name.', label='Full Name')
    address = forms.CharField(max_length=30, required=False, help_text='Your address.', label='Address')
    city = forms.CharField(max_length=30, required=True, help_text='Your city name.', label='City')
    easypaisa_account = forms.CharField(max_length=30,  help_text='Your easypaisa account', label='City')
    class Meta:
        model =  User
        fields =  ['username', 'name', 'city', 'easypaisa_account', 'address', 'email', 'password1', 'password2']
        
    def clean(self):
 
        super(CreatUserForm, self).clean()
         
        name = self.cleaned_data.get('name')
        address = self.cleaned_data.get('address')
        city = self.cleaned_data.get('city')
        username = self.cleaned_data.get('username')
        easypaisa_account = self.cleaned_data.get('easypaisa_account')
 
        if len(city) < 5:
            self._errors['city'] = self.error_class([
                'City minimum character should be 5.'])
        if len(name) < 4:
            self._errors['name'] = self.error_class([
                'Name should contain a minimum of 4 characters'])
        if len(username) < 4:
            self._errors['username'] = self.error_class([
                'Username should contain a minimum of 4 characters'])
        if len(address) < 5:
            self._errors['address'] = self.error_class([
                'Address can not be less 5 characters'])
        if len(easypaisa_account) != 11:
            self._errors['easypaisa_account'] = self.error_class([
                'Easypaisa account number should be 11'])
 
        return self.cleaned_data

class ServicesForm(ModelForm):
    
    class Meta:
        model = Services
        fields = '__all__'
        exclude = ['launderette']
    
    def clean(self):
 
        super(ServicesForm, self).clean()
         
        title = self.cleaned_data.get('title')
        price = self.cleaned_data.get('price')
 
        if price < 5:
            self._errors['price'] = self.error_class([
                'Minimum price can be 5.'])
        if len(title) < 5:
            self._errors['title'] = self.error_class([
                'Service Title Should Contain a minimum of 5 characters'])
 
        return self.cleaned_data


class LaundererForm(ModelForm):
    
    class Meta:
        model = Launderer
        fields = '__all__'
        exclude = ['user']       
    
    def clean(self):
 
        super(LaundererForm, self).clean()
         
        name = self.cleaned_data.get('name')
        address = self.cleaned_data.get('address')
        city = self.cleaned_data.get('city')
        easypaisa_account = self.cleaned_data.get('easypaisa_account')
 
        if len(city) < 5:
            self._errors['city'] = self.error_class([
                'City minimum character should be 5.'])
        if len(name) < 4:
            self._errors['name'] = self.error_class([
                'Name should contain a minimum of 4 characters'])
        if len(address) < 5:
            self._errors['address'] = self.error_class([
                'Address can not be less 5 characters'])
        if len(easypaisa_account) != 11:
            self._errors['easypaisa_account'] = self.error_class([
                'Easypaisa account number should be 11'])
 
        return self.cleaned_data


class LaunderetteForm(ModelForm):
    
    class Meta:
        model = Launderette
        fields = '__all__'
        exclude = ['launderer']
        
    def clean(self):
 
        super(LaunderetteForm, self).clean()
         
        name = self.cleaned_data.get('name')
        location = self.cleaned_data.get('location')
        available_time = self.cleaned_data.get('available_time')
 
        if len(available_time) < 5:
            self._errors['available_time'] = self.error_class([
                'Available time minimum character should be 5.'])
        if len(name) < 4:
            self._errors['name'] = self.error_class([
                'Name should contain a minimum of 4 characters'])
        if len(location) < 5:
            self._errors['location'] = self.error_class([
                'Location can not be less 5 characters'])
 
        return self.cleaned_data

class ReviewCommentForm(ModelForm):
    comment=forms.CharField(widget=forms.Textarea(attrs={"rows":5,  }))
    
    class Meta:
        model = ReviewComment
        exclude = '__all__'
        fields = ['comment']
    
    def clean(self):
 
        super(ReviewCommentForm, self).clean()
         
        comment = self.cleaned_data.get('comment')
 
        if len(comment) < 4:
            self._errors['comment'] = self.error_class([
                'Comment minimum character should be 4.'])


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
    response=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}), required=False)

    class Meta:
        model = Complaint
        fields = ["complain", "response", 'subject']
    
    def clean(self):
 
        super(ComplaintForm, self).clean()
         
        complain = self.cleaned_data.get('complain')
 
        if len(complain) < 4:
            self._errors['complain'] = self.error_class([
                'Complain minimum character should be 4.'])