# cms/views.py
import logging
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MastereData
from .forms import *


logger = logging.getLogger(__name__)


class ListingsView(LoginRequiredMixin, ListView):
    model = MastereData
    template_name = 'cms/listings.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        user_scope =  user.user_scope

        if user_scope in ["1", "2", "3", "4"]:  # Super Admin, Portal Admin, Portal Manager, Project Coordinator
            if search_query:
                queryset = queryset.filter(name__icontains=search_query)
        else:  # Other user scopes
            queryset = queryset.filter(created_by=user.uuid)
            if search_query:
                queryset = queryset.filter(name__icontains=search_query)
        
        return queryset


class AddListingView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MastereData
    form_class = MasterDataForm
    template_name = 'cms/add_listing.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Listing added successfully!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user.uuid
        form.instance.updated_by = self.request.user.uuid
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ViewListingView(LoginRequiredMixin, DetailView):
    model = MastereData
    template_name = 'cms/view_listing.html'
    context_object_name = 'listing'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except MastereData.DoesNotExist:
            messages.error(request, "Listing not found.")
            return redirect('cms:listings')
        

    
class EditListingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MastereData
    form_class = MasterDataForm
    template_name = 'cms/edit_listing.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Listing updated successfully!"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.uuid
        return super().form_valid(form)

class EditAddressView(LoginRequiredMixin, UpdateView):
    model = MastereData
    form_class = AddressForm
    template_name = 'cms/edit_address.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Address updated successfully!"

    def form_valid(self, form):
        try:
            form.instance.updated_by = self.request.user.uuid
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return self.form_invalid(form)
        

class EditTimingSocialView(LoginRequiredMixin, UpdateView):
    model = MastereData
    form_class = TimingSocialForm
    template_name = 'cms/edit_timing_social.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Timing and social media details updated successfully!"

    def form_valid(self, form):
        try:
            form.instance.updated_by = self.request.user.uuid
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return self.form_invalid(form)
        

class EditContactView(LoginRequiredMixin, UpdateView):
    model = MastereData
    form_class = ContactForm
    template_name = 'cms/edit_contact.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Contact details updated successfully!"

    def form_valid(self, form):
        try:
            form.instance.updated_by = self.request.user.uuid
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return self.form_invalid(form)
        

class EditPaymentView(LoginRequiredMixin, UpdateView):
    model = MastereData
    form_class = PaymentForm
    template_name = 'cms/edit_payment.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Payment details updated successfully!"

    def form_valid(self, form):
        try:
            form.instance.updated_by = self.request.user.uuid
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return self.form_invalid(form)
        


class EditAdditionalView(UpdateView):
    model = MastereData
    form_class = AdditionalDetailsForm
    template_name = 'cms/edit_additional.html'
    success_url = reverse_lazy('cms:listings')
    success_message = "Additional details updated successfully!"

    def get_context_data(self,form, **kwargs):
        form.instance.updated_by = self.request.user.uuid
        context = super().get_context_data(**kwargs)
        context['image_upload_form'] = SingleImageUploadForm()
        context['image_gallery'] = self.get_object().gallery.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure self.object is set
        if 'upload_image' in request.POST:
            image_form = SingleImageUploadForm(request.POST, request.FILES)
            if image_form.is_valid():
                image = image_form.save()
                self.object.gallery.add(image)
                messages.success(request, "Image uploaded successfully!")
                return redirect('cms:edit_additional', pk=self.object.pk)
            else:
                messages.error(request, "Error uploading image.")
        elif 'delete_image' in request.POST:
            image_id = request.POST.get('delete_image')
            image = get_object_or_404(ImageGallery, id=image_id)
            self.object.gallery.remove(image)
            image.delete()
            messages.success(request, "Image deleted successfully!")
            return redirect('cms:edit_additional', pk=self.object.pk)
        return super().post(request, *args, **kwargs)
    


class PoojaCreateView(CreateView):
    model = Poojas
    form_class = PoojaForm
    template_name = 'cms/add_pooja.html'

    def form_valid(self, form):
        form.instance.temple = get_object_or_404(MastereData, pk=self.kwargs['temple_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cms:list_poojas', kwargs={'temple_id': self.kwargs['temple_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temple_id'] = self.kwargs['temple_id']
        return context


class PoojaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Poojas
    form_class = PoojaForm
    template_name = 'cms/edit_pooja.html'
    context_object_name = 'pooja'
    success_message = "Pooja updated successfully!"

    def get_success_url(self):
        return reverse_lazy('cms:list_poojas', kwargs={'temple_id': self.object.temple.id})
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user.uuid
        return super().form_valid(form)


class PoojaListView(ListView):
    model = Poojas
    template_name = 'cms/list_poojas.html'
    context_object_name = 'poojas'

    def get_queryset(self):
        self.temple = get_object_or_404(MastereData, pk=self.kwargs['temple_id'])
        return Poojas.objects.filter(temple=self.temple)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temple_id'] = self.kwargs['temple_id']
        context['temple'] = self.temple
        return context

class BlogListView(ListView):
    model = Blog
    template_name = 'cms/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(Q(author=user) | Q(created_by=str(user.uuid)))

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'cms/blog_detail.html'
    context_object_name = 'blog'


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'cms/blog_form.html'
    success_url = reverse_lazy('cms:blog_list')
    success_message = "Blog created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        form.instance.created_by = str(self.request.user.uuid)
        form.instance.updated_by = str(self.request.user.uuid)
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'cms/blog_form.html'
    success_url = reverse_lazy('cms:blog_list')
    success_message = "Blog updated successfully!"

    def form_valid(self, form):
        form.instance.updated_by = str(self.request.user.uuid)
        response = super().form_valid(form)

        # Handle image removal
        if self.request.POST.getlist('remove_images'):
            for image_id in self.request.POST.getlist('remove_images'):
                image = get_object_or_404(ImageGallery, id=image_id)
                form.instance.images.remove(image)

        return response

