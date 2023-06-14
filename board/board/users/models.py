from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.


class ProfileModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profilemodel')
    image = models.ImageField(default='default.jpg', upload_to='static/uploads/', validators=[
                              FileExtensionValidator(['png', 'jpg'])])

    def __str__(self):
        return self.user.username
