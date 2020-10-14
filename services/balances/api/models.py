from django.db import models
from django.db.models import Sum


class BalanceManager(models.Manager):

    def points_sum(self, user_id):
        return super().filter(user_id=user_id).aggregate(Sum('points')).get('points__sum')


class Balance(models.Model):
    user_id = models.IntegerField()
    points = models.IntegerField()
    description = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Created')

    objects = BalanceManager()

    def __str__(self):
        return self.points
