# webapp/cms/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from utils.common.generators import generate_random_code
from django_ckeditor_5.fields import CKEditor5Field
from qrcode import make as qr_make  # For generating QR codes
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from utils.models import CommonFields
import logging

User = get_user_model()

logger = logging.getLogger("django")

def default_blank_fields():
    fields = []
    return fields

def get_user_id(instance):
    try:
        if instance.created_by:
            user_id = instance.created_by if instance.created_by else "01"
        else:
            user_id = "01"
        return user_id
    except:
        return "01"
    
def master_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/master_data/user_<id>/<filename>
    schema_name = "public"
    user_id = get_user_id(instance)
    print("Instance :", instance)
    path = f"{schema_name}/master_data/user_{user_id}/{instance.id}/{filename}"
    return path

def ad_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/ad_data/user_<id>/<filename>
    schema_name = "public"
    user_id = get_user_id(instance)
    path = f"{schema_name}/ad_data/user_{user_id}/{instance.id}/{filename}"
    return path


class ImageGallery(CommonFields):
    image = models.ImageField(upload_to=master_upload_directory_path,null=True)
    caption = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.caption if self.caption else str(self.uuid)

class Tag(CommonFields):
    name = models.CharField(max_length=255,null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Category(CommonFields):
    name = models.CharField(max_length=255,null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to=master_upload_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name

class Blog(CommonFields):
    title = models.CharField(max_length=120, null=True)
    slug = models.CharField(max_length=180, null=True, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    content = CKEditor5Field('Content')
    categories = models.ManyToManyField(Category, related_name='blogs', blank=True)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    thumbnail = models.ImageField(upload_to=master_upload_directory_path, null=True, blank=True)
    images = models.ManyToManyField(ImageGallery, related_name='blogs', blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MastereData(CommonFields):
    listing_data = (("Temple", "Temple"), ("Service", "Services"), ("Festivals", "Festivals"))

    # Basic details and category
    name = models.CharField(max_length=120, null=True)
    subtitle = models.CharField(max_length=225, null=True, blank=True)
    description = CKEditor5Field('Description')
    image = models.ImageField(upload_to=master_upload_directory_path, null=True, blank=True)
    deity = models.CharField(max_length=200, null=True, blank=True)
    deity_list = models.JSONField(default=default_blank_fields, null=True, blank=True)
    listing_type = models.CharField(max_length=225, choices=listing_data, default="Temple")
    categories = models.ManyToManyField(Category, related_name='masterdata')
    tags = models.ManyToManyField(Tag, related_name='masterdata')

    # Address details
    landmark = models.CharField(max_length=225, null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    town = models.CharField(max_length=225, null=True, blank=True)
    district = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)

    # Timing & social media
    time_slot_1 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_2 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_3 = models.CharField(max_length=225, null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True, default=default_blank_fields)
    facebook_page = models.URLField(null=True, blank=True)
    instagram_page = models.URLField(null=True, blank=True)
    twitter_page = models.URLField(null=True, blank=True)
    youtube_channel = models.URLField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

    # Contact details
    telephone = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=220)

    # Payment and Donations
    acc_number = models.CharField(max_length=40, null=True, blank=True)
    ifsc_code = models.CharField(max_length=40, null=True, blank=True)
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    account_name = models.CharField(max_length=140, null=True, blank=True)
    upi_id = models.CharField(max_length=80, null=True, blank=True)
    upi_qr = models.ImageField(upload_to=master_upload_directory_path, null=True, blank=True)

    # Additional Information
    gallery = models.ManyToManyField(ImageGallery, related_name='masterdata', blank=True)
    story = models.CharField(max_length=180, null=True, blank=True)  # Link to Blog URL or Blog UUID

    def save(self, *args, **kwargs):
        # Generate a slug if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.name)

        # Generate UPI QR code
        if self.upi_id and not self.upi_qr:
            qr_code = qr_make(self.upi_id)
            buffer = BytesIO()
            qr_code.save(buffer, format='PNG')
            self.upi_qr.save(f'upi_{self.name}.png', InMemoryUploadedFile(
                buffer, None, f'upi_{self.name}.png', 'image/png', sys.getsizeof(buffer), None
            ), save=False)
            buffer.close()

        super(MastereData, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def get_map_embed_url(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/embed/v1/place?key=YOUR_GOOGLE_MAPS_API_KEY&q={self.latitude},{self.longitude}"
        return ""
    

class Poojas(CommonFields):
    name = models.CharField(max_length=180, null=True)
    code = models.CharField(max_length=80, null=True, blank=True)  # Auto generated code
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(default=0.00, blank=True)
    remarks = models.CharField(max_length=220, null=True, blank=True)
    booking_available = models.BooleanField(default=False)
    temple = models.ForeignKey(MastereData, on_delete=models.CASCADE, related_name='poojas')

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'POOJA-{self.pk}'
        super(Poojas, self).save(*args, **kwargs)


class Package(CommonFields):
    package_name = models.CharField(max_length=255)
    package_validity_days = models.IntegerField()
    price = models.FloatField()
    tax_percentage = models.FloatField()
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.package_name


class Customer(CommonFields):
    customer_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    customer_address = models.TextField()
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=20)
    customer_tax = models.CharField(max_length=50, null=True, blank=True)
    customer_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.customer_name



class Advertisement(CommonFields):
    AD_TYPE_CHOICES = [
        ('SQUARE_IMAGE', 'Square Image'),
        ('BANNER', 'Banner'),
        ('VIDEO', 'Video'),
        ('PAGE', 'Page'),
        ('OTHER', 'Other'),
    ]

    ad_name = models.CharField(max_length=255)
    related_listing = models.OneToOneField(MastereData, on_delete=models.CASCADE, related_name='advertisement')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='advertisements')
    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='advertisements')
    ad_start_on = models.DateTimeField()
    ad_ends_on = models.DateTimeField()
    ad_banner_image_1 = models.ImageField(upload_to=ad_upload_directory_path, null=True, blank=True)
    ad_banner_image_2 = models.ImageField(upload_to=ad_upload_directory_path, null=True, blank=True)
    ad_video_url = models.URLField(null=True, blank=True)
    ad_text = models.CharField(max_length=500, null=True, blank=True)
    ad_landing_page = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.ad_name


class Payment(CommonFields):
    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
        ('UPI', 'UPI'),
        ('OTHER', 'Other'),

    ]
    TRANSACTION_STATUS_CHOICES = [
        ('DONE', 'Done'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),

    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='payments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    bank_ref_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES,default="PENDING")

    def __str__(self):
        return f'Payment {self.pk} - {self.customer.customer_name}'



# Create Django Signals
@receiver(pre_save, sender=Blog)
def set_blog_author(sender, instance, **kwargs):
    if not instance.author:
        instance.author = instance.user