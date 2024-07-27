from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView
from .forms import UserProfileForm,CustomPasswordChangeForm

class CustomLoginView(BaseLoginView):
    template_name = 'user/auth.html'

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'user/auth.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/profile.html')

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return render(request, 'user/profile.html', {'message': 'Profile updated successfully'})

    
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