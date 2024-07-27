# cms/urls.py
from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('listings/', views.ListingsView.as_view(), name='listings'),
    path('add-listing/', views.AddListingView.as_view(), name='add_listing'),
    path('view-listing/<int:pk>/', views.ViewListingView.as_view(), name='view_listing'),
    path('edit-listing/<int:pk>/', views.EditListingView.as_view(), name='edit_listing'),
    path('edit-address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),
    path('edit-timing-social/<int:pk>/', views.EditTimingSocialView.as_view(), name='edit_timing_social'),
    path('edit-contact/<int:pk>/', views.EditContactView.as_view(), name='edit_contact'), 
    path('edit-payment/<int:pk>/', views.EditPaymentView.as_view(), name='edit_payment'),
    path('edit-additional/<int:pk>/', views.EditAdditionalView.as_view(), name='edit_additional'),
    path('pooja/add/<int:temple_id>/', views.PoojaCreateView.as_view(), name='add_pooja'),
    path('pooja/edit/<int:pk>/', views.PoojaUpdateView.as_view(), name='edit_pooja'),
    path('poojas/<int:temple_id>/', views.PoojaListView.as_view(), name='list_poojas'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='view_blog'),
    path('blogs/add/', views.BlogCreateView.as_view(), name='add_blog'),
    path('blogs/edit/<int:pk>/', views.BlogUpdateView.as_view(), name='edit_blog'),

]
