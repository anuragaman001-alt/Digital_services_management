from django.db import models
from django.conf import settings
from services.models import Plan
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    activated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=self.plan.validity_days)
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def days_remaining(self):
        if self.expires_at and self.status == 'active':
            delta = self.expires_at - timezone.now()
            return max(0, delta.days)
        return 0

    def __str__(self):
        return f"{self.user.username} -> {self.plan.name} [{self.status}]"


class Invoice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            import random
            self.invoice_number = f"INV-{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.subscription.user.username}"
