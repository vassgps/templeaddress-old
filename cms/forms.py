# # cms/forms.py
from django import forms
from .models import MastereData,ImageGallery, Poojas, Blog
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms.widgets import ClearableFileInput, Select
from django_ckeditor_5.fields import CKEditor5Field

class MasterDataForm(forms.ModelForm):
    deity_list = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MastereData
        fields = ['name', 'listing_type', 'subtitle', 'description', 'deity', 'categories', 'tags', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditor5Widget(attrs={'class': 'form-control'}),
            'deity': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': ClearableFileInput(attrs={'class': 'form-control'})
        }

    def clean_deity_list(self):
        data = self.cleaned_data['deity_list']
        # Split the input by commas and strip any extra whitespace
        return [item.strip() for item in data.split(',') if item.strip()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['deity_list'].initial = ', '.join(self.instance.deity_list)


class AddressForm(forms.ModelForm):
    class Meta:
        model = MastereData
        fields = ['landmark', 'location', 'town', 'district', 'zipcode', 'state', 'country', 'latitude', 'longitude', 'map_url']
        widgets = {
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'map_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TimingSocialForm(forms.ModelForm):
    class Meta:
        model = MastereData
        fields = [
            'time_slot_1', 'time_slot_2', 'time_slot_3', 'social_media',
            'facebook_page', 'instagram_page', 'twitter_page',
            'youtube_channel', 'whatsapp_number'
        ]
        widgets = {
            'time_slot_1': forms.TextInput(attrs={'class': 'form-control'}),
            'time_slot_2': forms.TextInput(attrs={'class': 'form-control'}),
            'time_slot_3': forms.TextInput(attrs={'class': 'form-control'}),
            'social_media': forms.Textarea(attrs={'class': 'form-control'}),
            'facebook_page': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_page': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_page': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_channel': forms.URLInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = MastereData
        fields = [
            'telephone', 'mobile', 'email', 'website', 'slug'
        ]
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = MastereData
        fields = [
            'acc_number', 'ifsc_code', 'bank_name', 'account_name', 'upi_id', 'upi_qr'
        ]
        widgets = {
            'acc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control'}),
            'upi_qr': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SingleImageUploadForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = ImageGallery
        fields = ['image']

class AdditionalDetailsForm(forms.ModelForm):
    story = forms.CharField(widget=CKEditor5Widget(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = MastereData
        fields = ['story']

class PoojaForm(forms.ModelForm):
    class Meta:
        model = Poojas
        fields = ['name', 'description', 'amount', 'remarks', 'booking_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'booking_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())
    slug = forms.CharField(required=False)

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'tags', 'categories', 'thumbnail', 'images']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'categories': forms.CheckboxSelectMultiple(),
            'images': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False

