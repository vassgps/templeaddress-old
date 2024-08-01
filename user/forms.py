# webapp/user/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as BaseUserCreationForm
from .models import CustomUser


class UserProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'mobile_number')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username, Mobile, or Email", max_length=254)

class CustomUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'mobile_number', 'password1', 'password2')



class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        read_only_fields = ['uuid', 'username', 'created_at', 'created_by', 'updated_at', 'updated_by']
        for field in read_only_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True