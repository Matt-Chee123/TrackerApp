from django.db import models


class Account:
    account_name = models.CharField(max_length=30)
    user_id = models.ForeignKey('user.User',on_delete=models.CASCADE())
