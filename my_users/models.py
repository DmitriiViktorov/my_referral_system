from django.db import models
import random
import string


class MyUser(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def get_referred_users(self):
        return MyUser.objects.filter(referred_by=self).values_list('phone_number', flat=True)

    def __str__(self):
        return self.phone_number


