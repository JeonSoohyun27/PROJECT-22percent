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
    class State(models.IntegerChoices):
        TOBE_PAID = 1, '지급예정' 
        PAID      = 2, '지급완료'
        UNPAID    = 3, '미지급'

    users_deals   = models.ForeignKey('UserDeal', on_delete=models.PROTECT)
    principal     = models.IntegerField()
    interest      = models.IntegerField()
    tax           = models.IntegerField()
    commission    = models.IntegerField()
    payback_round = models.IntegerField()
    state         = models.IntegerField(choices=State.choices)
    payback_date  = models.DateField()

    class Meta:
        db_table = 'user_paybacks'

class DebtorPayback(TimeStampModel):
    class State(models.IntegerChoices):
        TOBE_PAID = 1, '지급예정' 
        PAID      = 2, '지급완료'
        UNPAID    = 3, '미지급'

    deal          = models.ForeignKey('deals.Deal', on_delete=models.PROTECT)
    principal     = models.IntegerField()
    interest      = models.IntegerField()
    payback_round = models.IntegerField()
    state         = models.IntegerField(choices=State.choices)
    payback_date  = models.DateField()

    class Meta:
        db_table = 'debtor_paybacks'
