from email.policy import default
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager

# Create your models here.
class Files(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="files")

    class Meta:
        db_table = "files"
