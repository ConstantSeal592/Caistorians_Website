from django.db import models
import calendar
from accounts.models import CustomUser

WEEKDAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]



class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.name

class Service(models.Model):
    salon = models.ForeignKey(Salon, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 9999.99 max
    duration_minutes = models.PositiveIntegerField()  # estimated time in minutes

    def __str__(self):
        return f"{self.name} - ${self.price} ({self.duration_minutes} mins)"


from django.db import models
import calendar

class OpeningHour(models.Model):
    salon = models.ForeignKey('Salon', related_name='regular_hours', on_delete=models.CASCADE)
    day = models.IntegerField(choices=[(i, calendar.day_name[i]) for i in range(7)])
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('salon', 'day')

    def __str__(self):
        return f"{self.salon.name} - {calendar.day_name[self.day]}"

class HolidayOpeningHour(models.Model):
    salon = models.ForeignKey('Salon', related_name='holiday_hours', on_delete=models.CASCADE)
    date = models.DateField()
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('salon', 'date')

    def __str__(self):
        return f"{self.salon.name} - {self.date} (Holiday Override)"



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.core.exceptions import ValidationError


from django.core.exceptions import ValidationError


class StaffShift(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)  # e.g. 0 = Monday
    start_time = models.TimeField()
    end_time = models.TimeField()
    repeat_weekly = models.BooleanField(default=False)
    
    def clean(self):

    # Don't run validation unless staff is assigned
        if not self.staff_id:
            return

        salon = self.staff.salon
        opening_hours = salon.regular_hours.filter(day=self.weekday)

        if not opening_hours.exists():
            raise ValidationError("This salon is not open on that day.")

        valid = False
        for hours in opening_hours:
            if not hours.is_closed and hours.open_time <= self.start_time and hours.close_time >= self.end_time:
                valid = True
                break

        if not valid:
            raise ValidationError("Shift must be within salon opening hours.")


    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation happens
        super().save(*args, **kwargs)

class StaffShiftException(models.Model):
    shift = models.ForeignKey(StaffShift, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)  # optional

    class Meta:
        unique_together = ('shift', 'date')

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from .models import StaffShift, HolidayOpeningHour

@receiver(post_save, sender=HolidayOpeningHour)
def remove_conflicting_shifts(sender, instance, **kwargs):
    if instance.is_closed:
        date = instance.date
        weekday = date.weekday()
        salon = instance.salon

        # Remove all repeating and one-time shifts that fall on that weekday
        conflicting_shifts = StaffShift.objects.filter(
            staff__salon=salon,
            weekday=weekday
        )

        # If repeat = False, also match against the specific date
        conflicting_shifts = conflicting_shifts.filter(
            models.Q(repeat=True) |
            models.Q(date=date)  # only if you store one-time shift dates (optional)
        )

        conflicting_shifts.delete()
