from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView
from utils.common.generators import generate_random_code
from .forms import UserProfileForm,CustomPasswordChangeForm,CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'user/auth.html'
    authentication_form = CustomAuthenticationForm

# class SignupView(View):
#     def get(self, request):
#         form = UserCreationForm()
#         return render(request, 'user/auth.html', {'form': form})

#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#         return render(request, 'user/auth.html', {'form': form})

class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user/auth.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_random_code()
            user.save()
            
            # Find the backend that should be used for this user
            backend = 'user.backends.CustomAuthBackend'
            login(request, user, backend=backend)
            
            return redirect('user:dashboard')
        return render(request, 'user/auth.html', {'form': form})
    

def logout_view(request):
    logout(request)
    return redirect('user:login')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'user/change_password.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'user/change_password.html', {'form': form})


# class ProfileView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, 'user/profile.html')

#     def post(self, request):
#         user = request.user
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.email = request.POST.get('email')
#         user.save()
#         return render(request, 'user/profile.html', {'message': 'Profile updated successfully'})

class ProfileView(View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'user/update_profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'user/update_profile.html', {'form': form})
    
#LoginRequiredMixin
class DashboardView(View):
    def get(self, request):
        return render(request, 'user/dashboard.html')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'user/update_profile.html'
    success_url = reverse_lazy('user:dashboard')

    def get_object(self, queryset=None):
        return self.request.user