from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser
from .forms import (
    UserRegistrationForm, CustomLoginForm, AdminUserCreateForm,
    AdminUserUpdateForm, UserProfileForm,
    PasswordResetRequestForm, SetNewPasswordForm
)
from .decorators import admin_required


# --- Registration ---

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Account created! Welcome.")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# --- Login / Logout ---

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# --- Password Reset (simple, no OTP) ---

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                request.session['reset_user_id'] = user.pk
                messages.info(request, "Email verified. Please set your new password.")
                return redirect('set_new_password')
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with that email.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def set_new_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            del request.session['reset_user_id']
            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'accounts/set_new_password.html', {'form': form})


# --- Dashboard ---

@login_required
def dashboard(request):
    if request.user.is_admin():
        from subscriptions.models import Subscription
        from services.models import Plan
        context = {
            'total_users': CustomUser.objects.filter(role='user').count(),
            'total_plans': Plan.objects.count(),
            'total_subscriptions': Subscription.objects.count(),
            'active_subscriptions': Subscription.objects.filter(status='active').count(),
            'recent_subscriptions': Subscription.objects.select_related('user', 'plan').order_by('-created_at')[:10],
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    else:
        from subscriptions.models import Subscription
        from services.models import Plan
        my_subs = Subscription.objects.filter(user=request.user).select_related('plan')
        context = {
            'my_subscriptions': my_subs,
            'wifi_plans': Plan.objects.filter(plan_type='wifi', is_active=True),
            'sim_plans': Plan.objects.filter(plan_type='sim', is_active=True),
            'ott_plans': Plan.objects.filter(plan_type='ott', is_active=True),
        }
        return render(request, 'accounts/user_dashboard.html', context)


# --- Admin — User Management ---

@login_required
@admin_required
def admin_user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/admin_user_list.html', {'users': users})


@login_required
@admin_required
def admin_user_create(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_user_list')
    else:
        form = AdminUserCreateForm()
    return render(request, 'accounts/admin_user_form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def admin_user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin_user_list')
    else:
        form = AdminUserUpdateForm(instance=user)
    return render(request, 'accounts/admin_user_form.html', {'form': form, 'action': 'Update', 'edit_user': user})


@login_required
@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted.")
        return redirect('admin_user_list')
    return render(request, 'accounts/admin_user_confirm_delete.html', {'edit_user': user})


# --- User Profile ---

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/user_profile.html', {'form': form})
