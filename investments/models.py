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

class PaybackSchedule(TimeStampModel):
    class Option(models.IntegerChoices):
        OPTION_1  = 5000
        OPTION_2  = 10000
        OPTION_3  = 20000
        OPTION_4  = 50000
        OPTION_5  = 100000
        OPTION_6  = 200000
        OPTION_7  = 300000
        OPTION_8  = 400000
        OPTION_9  = 500000
        OPTION_10 = 1000000
        OPTION_11 = 1500000
        OPTION_12 = 2000000
        OPTION_13 = 2500000
        OPTION_14 = 3000000
        OPTION_15 = 3500000
        OPTION_16 = 4000000
        OPTION_17 = 4500000
        OPTION_18 = 5000000
        OPTION_19 = 6000000
        OPTION_20 = 7000000
        OPTION_21 = 8000000
        OPTION_22 = 9000000
        OPTION_23 = 10000000

    deal          = models.ForeignKey('deals.Deal', on_delete=models.PROTECT)
    option        = models.IntegerField(choices=Option.choices)
    principal     = models.IntegerField()
    interest      = models.IntegerField()
    tax           = models.IntegerField()
    commission    = models.IntegerField()
    payback_round = models.IntegerField()
    payback_date  = models.DateField()

    class Meta:
        db_table = 'payback_schedules'
