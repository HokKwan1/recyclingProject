from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.
class Request(models.Model):
  STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
  
  first_name = models.CharField(max_length=256)
  last_name = models.CharField(max_length=256)
  email = models.EmailField(max_length=256)
  phone = models.CharField(max_length=20)
  address = models.CharField(max_length=256)
  city = models.CharField(max_length=64)
  state = models.CharField(max_length=64)
  country = models.CharField(max_length=64)
  postal_code = models.CharField(max_length=64)
  status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
  date_created = models.DateTimeField(auto_now_add=False)
  date_completed = models.DateTimeField(null=True, blank=True)
  token = models.CharField(max_length=512)
  claimed_by = models.ForeignKey(AuthUser, null=True, blank=True, on_delete=models.SET_NULL, related_name="claimed_requests")

  def __str__(self):
    return self.first_name + " " + self.last_name