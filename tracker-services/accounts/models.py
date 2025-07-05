from django.db import models


class Account(models.Model):
    account_name = models.CharField(max_length=30)
    user_id  = models.ForeignKey('user.User',on_delete=models.CASCADE)

    class Meta:
        db_table = "user_account"
