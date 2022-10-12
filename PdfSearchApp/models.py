from django.db import models

# Create your models here.
class Files(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="files")

    class Meta:
        db_table = "files"
