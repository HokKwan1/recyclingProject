from django.db import models

# Create your models here.
class Request(models.Model):
  first_name = models.CharField(max_length=256)
  last_name = models.CharField(max_length=256)
  email = models.CharField(max_length=256)
  phone = models.CharField(max_length=20)
  address = models.CharField(max_length=256)
  city = models.CharField(max_length=64)
  state = models.CharField(max_length=64)
  country = models.CharField(max_length=64)
  postal_code = models.CharField(max_length=64)
  status = models.CharField(max_length=32)
  date_created = models.DateField(auto_now_add=True)
  date_completed = models.DateField(null=True, blank=True)
  token = models.CharField(max_length=512)
  claimed_by = models.CharField(max_length=12, null=True, blank=True)

  def __str__(self):
    return self.first_name + " " + self.last_name