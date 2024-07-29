# webapp/cms/admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .forms import MasterDataForm
from .models import (
    ImageGallery,
    Tag,
    Category,
    Blog,
    MastereData,
    Poojas,
    Package,
    Customer,
    Advertisement,
    Payment,
)

class MastereDataResource(resources.ModelResource):
    class Meta:
        model = MastereData

class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog

# class MastereDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     # form = MasterDataForm
#     resource_class = MastereDataResource
#     list_display = ('name', 'listing_type', 'location', 'district','country', 'created_by', 'updated_at')
#     list_filter = ('listing_type', 'categories', 'tags')
#     search_fields = ('name', 'description', 'location', 'district', 'state', 'country')
#     readonly_fields = ('uuid', 'created_by', 'created_at', 'updated_by', 'updated_at')

class MastereDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # form = MasterDataForm
    resource_class = MastereDataResource
    list_display = ('name', 'listing_type', 'location', 'district', 'country', 'created_by', 'updated_at')
    list_filter = ('listing_type', 'categories', 'tags')
    search_fields = ('name', 'description', 'location', 'district', 'state', 'country')
    readonly_fields = ('uuid', 'listing_type', 'created_by', 'created_at', 'updated_by', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'name', 'subtitle', 'description', 'deity', 'categories', 'tags', 'image', 'gallery', 
                'story', 'listing_type', 'location', 'district', 'state', 'country', 'latitude', 'longitude',
                'uuid', 'created_by', 'created_at', 'updated_by', 'updated_at'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.uuid
        obj.updated_by = request.user.uuid
        super().save_model(request, obj, form, change)

class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BlogResource
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'categories', 'tags')
    search_fields = ('title', 'content', 'author__username')


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image', 'created_at', 'updated_at')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'icon', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}

class PoojasAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'amount', 'booking_available', 'temple', 'created_at', 'updated_at')
    list_filter = ('temple', 'booking_available')
    search_fields = ('name', 'code', 'description', 'temple__name')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'package_validity_days', 'price', 'tax_percentage', 'created_at', 'updated_at')
    search_fields = ('package_name',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'user', 'customer_email', 'customer_mobile', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'customer_email', 'customer_mobile', 'customer_address')

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('ad_name', 'related_listing', 'customer', 'ad_type', 'ad_start_on', 'ad_ends_on', 'created_at', 'updated_at')
    list_filter = ('ad_type', 'package')
    search_fields = ('ad_name', 'ad_text', 'customer__customer_name', 'related_listing__name')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'package', 'advertisement', 'amount', 'payment_mode', 'transaction_status', 'created_at', 'updated_at')
    list_filter = ('payment_mode', 'transaction_status')
    search_fields = ('customer__customer_name', 'advertisement__ad_name', 'transaction_id', 'bank_ref_id')

admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(MastereData, MastereDataAdmin)
admin.site.register(Poojas, PoojasAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Payment, PaymentAdmin)
