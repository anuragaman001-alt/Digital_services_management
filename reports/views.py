from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from subscriptions.models import Subscription, Invoice
from services.models import Plan
from accounts.models import CustomUser
from accounts.decorators import admin_required
from django.db.models import Count, Sum
from django.utils import timezone
import csv


@login_required
@admin_required
def sales_report(request):
    plan_type = request.GET.get('type', '')
    status = request.GET.get('status', '')

    subs = Subscription.objects.select_related('user', 'plan').order_by('-created_at')
    if plan_type:
        subs = subs.filter(plan__plan_type=plan_type)
    if status:
        subs = subs.filter(status=status)

    total_revenue = Invoice.objects.filter(
        subscription__in=subs, paid=True
    ).aggregate(total=Sum('amount'))['total'] or 0

    plan_breakdown = (
        subs.values('plan__plan_type')
        .annotate(count=Count('id'))
        .order_by('plan__plan_type')
    )

    context = {
        'subscriptions': subs,
        'total_revenue': total_revenue,
        'total_subs': subs.count(),
        'active_subs': subs.filter(status='active').count(),
        'plan_breakdown': plan_breakdown,
        'plan_type': plan_type,
        'status_filter': status,
    }
    return render(request, 'reports/sales_report.html', context)


@login_required
@admin_required
def export_sales_csv(request):
    plan_type = request.GET.get('type', '')
    status = request.GET.get('status', '')

    subs = Subscription.objects.select_related('user', 'plan').order_by('-created_at')
    if plan_type:
        subs = subs.filter(plan__plan_type=plan_type)
    if status:
        subs = subs.filter(status=status)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{timezone.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Digital Services Management - Sales Report'])
    writer.writerow(['Generated', timezone.now().strftime('%d-%m-%Y %H:%M')])
    writer.writerow([''])
    writer.writerow(['Sub ID', 'Customer', 'Email', 'Phone', 'Plan', 'Type',
                     'Price', 'Status', 'Activated On', 'Expires On', 'Days Remaining'])

    for sub in subs:
        writer.writerow([
            sub.pk,
            sub.user.get_full_name() or sub.user.username,
            sub.user.email,
            sub.user.phone or '',
            sub.plan.name,
            sub.plan.get_plan_type_display(),
            sub.plan.price,
            sub.get_status_display(),
            sub.activated_at.strftime('%d-%m-%Y'),
            sub.expires_at.strftime('%d-%m-%Y') if sub.expires_at else '',
            sub.days_remaining(),
        ])

    writer.writerow([''])
    total_revenue = Invoice.objects.filter(subscription__in=subs, paid=True).aggregate(
        total=Sum('amount'))['total'] or 0
    writer.writerow(['Total Revenue', f'Rs.{total_revenue}'])
    return response
