from django.db  import models

from core.models    import TimeStampModel

class Deal(TimeStampModel):
    name             = models.CharField(max_length=100)
    category         = models.ForeignKey('Category', on_delete=models.PROTECT)
    grade            = models.ForeignKey('DealGrade', on_delete=models.PROTECT)
    earning_rate     = models.DecimalField(max_digits=4, decimal_places=2)
    repayment_period = models.IntegerField()
    repayment_method = models.ForeignKey('RepaymentMethod', on_delete=models.PROTECT)
    net_amount       = models.IntegerField()
    repayment_day    = models.IntegerField()
    start_date       = models.DateField()
    end_date         = models.DateField(null=True)
    reason           = models.CharField(max_length=100)
    debtor           = models.ForeignKey('Debtor', on_delete=models.PROTECT)
    deal_status      = models.ForeignKey('DealStatus', on_delete=models.PROTECT)

    class Meta:
        db_table = 'deals'

class Debtor(TimeStampModel):
    name       = models.CharField(max_length=100)
    birth_date = models.DateField()

    class Meta:
        db_table = 'debtors'

class CreditScore(TimeStampModel):
    debtor      = models.ForeignKey('Debtor', on_delete=models.CASCADE)
    score       = models.IntegerField()
    credit_date = models.DateField()

    class Meta:
        db_table = 'credit_scores'

class DealGrade(TimeStampModel):
    grade = models.CharField(max_length=10)

    class Meta:
        db_table = 'deal_grades'

class DealStatus(TimeStampModel):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'deal_statuses'

class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class RepaymentMethod(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'repayment_methods'

class Mortgage(TimeStampModel):
    deal               = models.ForeignKey('Deal', on_delete=models.CASCADE)
    latitude           = models.DecimalField(max_digits=9, decimal_places=6)
    longitude          = models.DecimalField(max_digits=9, decimal_places=6)
    ltv_ratio          = models.DecimalField(max_digits=4, decimal_places=2)
    appraised_value    = models.IntegerField()
    senior_loan_amount = models.IntegerField()
    address            = models.TextField()
    completed_date     = models.DateField()
    scale              = models.CharField(max_length=100)
    supply_area        = models.DecimalField(max_digits=10, decimal_places=2)
    using_area         = models.DecimalField(max_digits=10, decimal_places=2)
    floors             = models.CharField(max_length=100)
    is_usage           = models.BooleanField()
    selling_point      = models.ForeignKey('SellingPoint', on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = 'mortgages'

class SellingPoint(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'selling_points'

class MortgageImage(models.Model):
    mortgage  = models.ForeignKey('Mortgage', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'mortgage_images'
