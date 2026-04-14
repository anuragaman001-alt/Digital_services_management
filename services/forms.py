from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        # Optional field hints
        self.fields['speed_mbps'].required = False
        self.fields['data_limit_gb'].required = False
        self.fields['calls'].required = False
        self.fields['sms'].required = False
        self.fields['mobile_data_gb'].required = False
        self.fields['streams'].required = False
        self.fields['resolution'].required = False
        self.fields['platforms'].required = False
