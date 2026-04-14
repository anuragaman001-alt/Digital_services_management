from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Subscription, Invoice
from services.models import Plan
from accounts.decorators import admin_required
from django.core.mail import send_mail
from django.conf import settings
import csv


# --- User: Subscribe ---

@login_required
def subscribe(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    if request.method == 'POST':
        existing = Subscription.objects.filter(
            user=request.user,
            plan__plan_type=plan.plan_type,
            status='active'
        ).first()
        if existing:
            messages.warning(request, f"You already have an active {plan.get_plan_type_display()} plan. Deactivate it first or upgrade/downgrade.")
            return redirect('plan_detail', pk=plan_id)

        sub = Subscription.objects.create(user=request.user, plan=plan, status='active')
        invoice = Invoice.objects.create(subscription=sub, amount=plan.price)
        messages.success(request, f"Successfully subscribed to {plan.name}! Invoice: {invoice.invoice_number}")
        return redirect('my_subscriptions')
    return render(request, 'subscriptions/confirm_subscribe.html', {'plan': plan})


@login_required
def my_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related('plan').order_by('-created_at')
    return render(request, 'subscriptions/my_subscriptions.html', {'subscriptions': subscriptions})


@login_required
def deactivate_subscription(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.status = 'inactive'
        sub.save()
        messages.success(request, f"Subscription to {sub.plan.name} deactivated.")
        return redirect('my_subscriptions')
    return render(request, 'subscriptions/confirm_deactivate.html', {'sub': sub})


@login_required
def reactivate_subscription(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.status = 'active'
        sub.save()
        messages.success(request, f"Subscription to {sub.plan.name} reactivated.")
        return redirect('my_subscriptions')
    return render(request, 'subscriptions/confirm_reactivate.html', {'sub': sub})


@login_required
def upgrade_downgrade(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    same_type_plans = Plan.objects.filter(plan_type=sub.plan.plan_type, is_active=True).exclude(pk=sub.plan.pk)
    if request.method == 'POST':
        new_plan_id = request.POST.get('new_plan_id')
        new_plan = get_object_or_404(Plan, pk=new_plan_id, is_active=True)
        sub.plan = new_plan
        sub.status = 'active'
        from django.utils import timezone
        from datetime import timedelta
        sub.expires_at = timezone.now() + timedelta(days=new_plan.validity_days)
        sub.save()
        invoice = Invoice.objects.create(subscription=sub, amount=new_plan.price)
        messages.success(request, f"Plan changed to {new_plan.name}.")
        return redirect('my_subscriptions')
    return render(request, 'subscriptions/upgrade_downgrade.html', {
        'sub': sub, 'same_type_plans': same_type_plans
    })


# --- Invoice ---

@login_required
def download_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, subscription__user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Digital Services Management'])
    writer.writerow([''])
    writer.writerow(['Invoice Number', invoice.invoice_number])
    writer.writerow(['Customer', invoice.subscription.user.get_full_name() or invoice.subscription.user.username])
    writer.writerow(['Email', invoice.subscription.user.email])
    writer.writerow(['Plan', invoice.subscription.plan.name])
    writer.writerow(['Plan Type', invoice.subscription.plan.get_plan_type_display()])
    writer.writerow(['Validity', f"{invoice.subscription.plan.validity_days} days"])
    writer.writerow(['Amount', f"Rs.{invoice.amount}"])
    writer.writerow(['Date', invoice.generated_at.strftime('%d-%m-%Y %H:%M')])
    writer.writerow(['Status', 'Paid' if invoice.paid else 'Pending'])
    return response


# --- Admin: Manage Subscriptions ---

@login_required
@admin_required
def admin_subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').order_by('-created_at')
    plan_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    if plan_type:
        subscriptions = subscriptions.filter(plan__plan_type=plan_type)
    if status:
        subscriptions = subscriptions.filter(status=status)
    return render(request, 'subscriptions/admin_subscription_list.html', {
        'subscriptions': subscriptions, 'plan_type': plan_type, 'status_filter': status
    })


@login_required
@admin_required
def admin_toggle_subscription(request, pk):
    sub = get_object_or_404(Subscription, pk=pk)
    if sub.status == 'active':
        sub.status = 'inactive'
    else:
        sub.status = 'active'
    sub.save()
    messages.success(request, f"Subscription status changed to {sub.status}.")
    return redirect('admin_subscription_list')
