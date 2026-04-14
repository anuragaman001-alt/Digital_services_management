from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan
from .forms import PlanForm
from accounts.decorators import admin_required


# ─── Public/User views ────────────────────────────────────────────────────────

@login_required
def plan_list(request):
    plan_type = request.GET.get('type', 'wifi')
    plans = Plan.objects.filter(plan_type=plan_type, is_active=True)
    return render(request, 'services/plan_list.html', {
        'plans': plans,
        'plan_type': plan_type,
        'wifi_count': Plan.objects.filter(plan_type='wifi', is_active=True).count(),
        'sim_count': Plan.objects.filter(plan_type='sim', is_active=True).count(),
        'ott_count': Plan.objects.filter(plan_type='ott', is_active=True).count(),
    })


@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    from subscriptions.models import Subscription
    user_sub = None
    if not request.user.is_admin():
        user_sub = Subscription.objects.filter(
            user=request.user, plan=plan, status='active'
        ).first()
    return render(request, 'services/plan_detail.html', {'plan': plan, 'user_sub': user_sub})


# ─── Admin views ──────────────────────────────────────────────────────────────

@login_required
@admin_required
def admin_plan_list(request):
    plan_type = request.GET.get('type', 'all')
    if plan_type == 'all':
        plans = Plan.objects.all()
    else:
        plans = Plan.objects.filter(plan_type=plan_type)
    return render(request, 'services/admin_plan_list.html', {
        'plans': plans, 'plan_type': plan_type
    })


@login_required
@admin_required
def admin_plan_create(request):
    plan_type = request.GET.get('type', 'wifi')
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Plan created successfully.")
            return redirect('admin_plan_list')
    else:
        form = PlanForm(initial={'plan_type': plan_type})
    return render(request, 'services/admin_plan_form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def admin_plan_update(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Plan updated.")
            return redirect('admin_plan_list')
    else:
        form = PlanForm(instance=plan)
    return render(request, 'services/admin_plan_form.html', {'form': form, 'action': 'Update', 'plan': plan})


@login_required
@admin_required
def admin_plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Plan deleted.")
        return redirect('admin_plan_list')
    return render(request, 'services/admin_plan_confirm_delete.html', {'plan': plan})


@login_required
@admin_required
def admin_plan_toggle(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.is_active = not plan.is_active
    plan.save()
    status = "activated" if plan.is_active else "deactivated"
    messages.success(request, f"Plan {status}.")
    return redirect('admin_plan_list')
