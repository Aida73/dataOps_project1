from django.db import models

# Create your models here.

class UserProfile(models.Model):

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'