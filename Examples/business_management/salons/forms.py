from django import forms
from .models import *
from django import forms
from django.forms import modelformset_factory
from .models import OpeningHour


class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['name', 'address', 'phone_number', 'email', 'website', 'description']



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'duration_minutes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
        }


OpeningHourFormSet = modelformset_factory(
    OpeningHour,
    fields=('day', 'open_time', 'close_time'),
    extra=0,
    can_delete=True,
    widgets={
        'day': forms.Select(attrs={'class': 'form-control'}),
        'open_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        'close_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
    }
)

from django import forms
from .models import HolidayOpeningHour

class HolidayOpeningHourForm(forms.ModelForm):
    class Meta:
        model = HolidayOpeningHour
        fields = ['date', 'open_time', 'close_time', 'is_closed']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
        }

from django import forms
from .models import StaffShift, OpeningHour

class StaffShiftForm(forms.ModelForm):
    class Meta:
        model = StaffShift
        fields = ['weekday', 'start_time', 'end_time', 'repeat_weekly']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        weekday = cleaned_data.get('weekday')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if not weekday or not start_time or not end_time:
            return cleaned_data

        salon = self.user.salon
        opening_hours = OpeningHour.objects.filter(salon=salon, weekday=weekday)

        for period in opening_hours:
            if period.open_time <= start_time and period.close_time >= end_time:
                return cleaned_data

        raise forms.ValidationError("This shift is outside the salon's opening hours.")

