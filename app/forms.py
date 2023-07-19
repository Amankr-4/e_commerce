from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from .models import customer

class customerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))  #dono password fields models ke ander nhi aate ye forms ke part h thats way isko alag se yaha likhna parta h
    password2 = forms.CharField(label="Confirm Password(again)",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(required=True,label="First Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False,label="Last Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email'] 
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))        



#  we can directly use these classes but we want to apply bootstrap that's why we are inhereting it
class password_change(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label="New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())  #dono password fields models ke ander nhi aate ye forms ke part h thats way isko alag se yaha likhna parta h
    new_password2 = forms.CharField(label="Confirm New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class password_reset_form(PasswordResetForm):
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
    
    
class password_confirm_form(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())  #dono password fields models ke ander nhi aate ye forms ke part h thats way isko alag se yaha likhna parta h
    new_password2 = forms.CharField(label="Confirm New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name' , 'locality' , 'city' , 'state' , 'zipcode']
        widgets = {
                   'name':forms.TextInput(attrs = {'class':'form-control'}),
                   'locality':forms.TextInput(attrs = {'class':'form-control'}),
                   'city':forms.TextInput(attrs = {'class':'form-control'}),
                   'state':forms.Select(attrs = {'class':'form-control'}),
                   'zipcode':forms.NumberInput(attrs = {'class':'form-control'})
                   }
