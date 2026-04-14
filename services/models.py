from django.db import models


class Plan(models.Model):
    PLAN_TYPE_CHOICES = (
        ('wifi', 'WiFi'),
        ('sim', 'SIM'),
        ('ott', 'OTT'),
    )
    VALIDITY_CHOICES = (
        (7, '7 Days'),
        (28, '28 Days'),
        (30, '30 Days'),
        (90, '90 Days'),
        (180, '180 Days'),
        (365, '365 Days'),
    )

    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    validity_days = models.IntegerField(choices=VALIDITY_CHOICES, default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # WiFi specific
    speed_mbps = models.IntegerField(blank=True, null=True, help_text="Speed in Mbps")
    data_limit_gb = models.IntegerField(blank=True, null=True, help_text="Data limit in GB, null=unlimited")

    # SIM specific
    calls = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Unlimited, 100 mins")
    sms = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 100 SMS, Unlimited")
    mobile_data_gb = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

    # OTT specific
    streams = models.IntegerField(blank=True, null=True, help_text="Simultaneous streams")
    resolution = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. HD, 4K")
    platforms = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. Web, Mobile, TV")

    class Meta:
        ordering = ['plan_type', 'price']

    def __str__(self):
        return f"{self.get_plan_type_display()} — {self.name} (₹{self.price})"

    def get_badge_class(self):
        return {'wifi': 'primary', 'sim': 'success', 'ott': 'danger'}.get(self.plan_type, 'secondary')
