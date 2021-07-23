import re

from django.db  import models

from core.models    import TimeStampModel

EMAIL_REGEX    = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

class User(TimeStampModel):
    email                     = models.CharField(max_length=100, unique=True, null=True)
    password                  = models.CharField(max_length=200, null=True)
    name                      = models.CharField(max_length=100, null=True)
    kakao_id                  = models.IntegerField(unique=True, null=True)
    deposit_amount            = models.IntegerField(default=0)
    deposit_account           = models.CharField(max_length=50, unique=True)
    deposit_bank              = models.ForeignKey('Bank', related_name='deposit_bank', on_delete=models.PROTECT)
    withdrawal_account        = models.CharField(max_length=50, unique=True, null=True)
    withdrawal_bank           = models.ForeignKey('Bank', related_name='withdrawal_bank', on_delete=models.PROTECT, null=True)
    net_invest_limit          = models.IntegerField(default=30000000)
    net_mortgage_invest_limit = models.IntegerField(default=10000000)
    credit_invest_limit       = models.IntegerField(default=1000000)
    mortgage_invest_limit     = models.IntegerField(default=5000000)
    deal                      = models.ManyToManyField('deals.Deal', through='investments.UserDeal')
    is_activate               = models.BooleanField(default=True)

    @staticmethod
    def validate_regex(data):    
        if not re.match(EMAIL_REGEX, data['email']):
            return False

        if not re.match(PASSWORD_REGEX, data['password']):
            return False 

        return True

    class Meta:
        db_table = 'users'

class Bank(TimeStampModel):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'banks'
