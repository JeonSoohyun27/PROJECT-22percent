from django.utils.translation import gettext_lazy as _
from django.db                import models

from core.models    import TimeStampModel

class Deal(TimeStampModel):
    class Category(models.IntegerChoices):
        MORTGAGE = 1, _('Mortgage')
        CREDIT   = 2, _('Credit')
        SPECIAL  = 3, _('Special')
        COMPANY  = 4, _('Company')
        ETC      = 5, _('etc')

    class Grade(models.IntegerChoices):
        A_PLUS  = 1, 'A+'
        A       = 2, 'A'
        A_MINUS = 3, 'A-'
        B_PLUS  = 4, 'B+'
        B       = 5, 'B'
        B_MINUS = 6, 'B-'
        C_PLUS  = 7, 'C+'
        C       = 8, 'C'
        C_MINUS = 9, 'C-'
        D_PLUS  = 10, 'D+'
        D       = 11, 'D'
        D_MINUS = 12, 'D-'

    class Status(models.IntegerChoices):
        APPLYING              = 1, _('Applying')
        NORMAL                = 2, _('Normal repayment')
        DELAY                 = 3, _('Delay')
        OVERDUE               = 4, _('Overdue')
        NONPERFORM            = 5, _('Nonperforming loan')
        NORMAL_COMPLETION     = 6, _('Normal repayment completed')
        NONPERFORM_COMPLETION = 7, _('Nonperforming loan completed')

    class RepaymentMethod(models.IntegerChoices):
        MIX             = 1, _('Mix')
        EQUAL_SUM       = 2, _('Equal principal and interest')
        MATURE          = 3, _('Redemption at maturity')
        EQUAL_PRINCIPAL = 4, _('Equal repayment of principal')

    name             = models.CharField(max_length=100)
    category         = models.IntegerField(choices=Category.choices)
    grade            = models.IntegerField(choices=Grade.choices)
    earning_rate     = models.DecimalField(max_digits=4, decimal_places=2)
    repayment_period = models.IntegerField()
    repayment_method = models.IntegerField(choices=RepaymentMethod.choices)
    net_amount       = models.IntegerField()
    repayment_day    = models.IntegerField()
    start_date       = models.DateField()
    end_date         = models.DateField(null=True)
    reason           = models.CharField(max_length=100)
    debtor           = models.ForeignKey('Debtor', on_delete=models.PROTECT)
    status           = models.IntegerField(choices=Status.choices)

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

class RepaymentMethod(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'repayment_methods'

class Mortgage(TimeStampModel):
    deal                      = models.ForeignKey('Deal', on_delete=models.CASCADE)
    latitude                  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude                 = models.DecimalField(max_digits=9, decimal_places=6)
    estimated_recovery        = models.IntegerField()
    appraised_value           = models.IntegerField()
    senior_loan_amount        = models.IntegerField()
    address                   = models.TextField()
    completed_date            = models.DateField()
    scale                     = models.CharField(max_length=100)
    supply_area               = models.DecimalField(max_digits=10, decimal_places=2)
    using_area                = models.DecimalField(max_digits=10, decimal_places=2)
    floors                    = models.CharField(max_length=100)
    is_usage                  = models.BooleanField()
    selling_point_title       = models.CharField(max_length=100)
    selling_point_description = models.TextField()

    class Meta:
        db_table = 'mortgages'

class MortgageImage(models.Model):
    mortgage  = models.ForeignKey('Mortgage', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'mortgage_images'
