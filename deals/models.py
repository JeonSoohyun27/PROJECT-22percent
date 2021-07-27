from django.db  import models

from core.models    import TimeStampModel

class Deal(TimeStampModel):
    class Category(models.IntegerChoices):
        MORTGAGE = 1, '부동산 담보대출' 
        CREDIT   = 2, '개인신용'
        SPECIAL  = 3, '스페셜딜'
        COMPANY  = 4, '기업'
        ETC      = 5, '기타'

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
        APPLYING              = 1, '신청중' 
        NORMAL                = 2, '정상'
        DELAY                 = 3, '상환지연'
        OVERDUE               = 4, '연체'
        NONPERFORM            = 5, '부실'
        NORMAL_COMPLETION     = 6, '정상상환완료'
        NONPERFORM_COMPLETION = 7, '부실상환완료'
        SCHEDULED             = 8, '모집예정'

    class RepaymentMethod(models.IntegerChoices):
        MIX             = 1, '혼합'
        EQUAL_SUM       = 2, '원리금균등'
        MATURE          = 3, '만기상환'
        EQUAL_PRINCIPAL = 4, '원금균등'

    name             = models.CharField(max_length=100)
    category         = models.IntegerField(choices=Category.choices)
    grade            = models.IntegerField(choices=Grade.choices)
    earning_rate     = models.DecimalField(max_digits=4, decimal_places=2)
    interest_rate    = models.DecimalField(max_digits=4, decimal_places=2)
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