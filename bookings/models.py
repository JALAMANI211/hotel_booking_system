from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hotel_name = models.CharField(max_length=100)
    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField()
    num_persons = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.hotel_name} ({self.check_in_datetime.date()})"