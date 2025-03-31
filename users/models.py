from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
