from django.db  import models

from core.models    import TimeStampModel

class UserDeal(TimeStampModel):
    user       = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    deal       = models.ForeignKey('deals.Deal', on_delete=models.SET_NULL, null=True)
    amount     = models.IntegerField()

    class Meta:
        db_table = 'users_deals'
        constraints = [ 
            models.UniqueConstraint(fields=['user', 'deal'], name='unique_user_deal')
        ]

class UserPayback(TimeStampModel):
    users_deals   = models.ForeignKey('UserDeal', on_delete=models.PROTECT)
    principal     = models.IntegerField()
    interest      = models.IntegerField()
    tax           = models.IntegerField()
    commission    = models.IntegerField()
    payback_round = models.IntegerField()
    state         = models.ForeignKey('PaybackState', on_delete=models.PROTECT)
    payback_date  = models.DateField()

    class Meta:
        db_table = 'user_paybacks'

class PaybackState(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'payback_states'

class DebtorPayback(TimeStampModel):
    deal          = models.ForeignKey('deals.Deal', on_delete=models.PROTECT)
    principal     = models.IntegerField()
    interest      = models.IntegerField()
    payback_round = models.IntegerField()
    state         = models.ForeignKey('PaybackState', on_delete=models.PROTECT)
    payback_date  = models.DateField()

    class Meta:
        db_table = 'debtor_paybacks'
