from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def set_file_upload_to(self, filename):
        return f'{self.user}/{filename}'

    image = models.FileField(upload_to=set_file_upload_to)

    class Meta:
        verbose_name = 'user image'
        verbose_name_plural = 'user images'
        db_table = "images"




