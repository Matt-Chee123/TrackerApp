from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['username','email','password']

    class Meta:
        db_table = "user_profile"