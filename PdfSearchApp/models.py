from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Files(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="files")
    filetype = models.CharField(max_length=50, default="")

    class Meta:
        db_table = "files"


class WordFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField()

    class Meta:
        db_table = "wordfiles"
