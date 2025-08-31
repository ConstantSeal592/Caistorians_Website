from django import forms
from .models import ArtistProfile, Product, SellerVideo 
from django.contrib.auth.models import User

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = ['bio', 'profile_picture']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        }

class SellerVideoForm(forms.ModelForm):
    class Meta:
        model = SellerVideo
        fields = ['title', 'video']  # Use 'video', NOT 'video_file'

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
