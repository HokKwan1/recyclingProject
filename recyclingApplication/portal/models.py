from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name
    
class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Roles'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'role',
                    'user'
                ],
                name='unique_role_user'
            )
        ]

    def __str__(self):
        return f'{self.role}'
