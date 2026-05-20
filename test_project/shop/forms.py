from django import forms
from django.contrib.auth import get_user_model

from shop.models import Ad, User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone_number', 'password']
    def clean(self):
        cleaned= super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','avatar_path', 'phone_number', 'full_name']
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password")
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm New Password")
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('new_password_confirm'):
            raise forms.ValidationError("New passwords do not match.")
        if cleaned.get('old_password') == cleaned.get('new_password'):
            raise forms.ValidationError("New password cannot be the same as the old password.")
        return cleaned
class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['brand', 'model', 'year', 'price', 'image_path', 'description', 'status']