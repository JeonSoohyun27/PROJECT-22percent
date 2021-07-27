from datetime import datetime, timedelta

from django.test  import TestCase, Client

from users.models       import Bank, User
from investments.models import UserDeal, UserPayback
from deals.models       import (
    Deal, 
    Debtor,
    MortgageImage, 
    Mortgage,
    CreditScore
)

class DealDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Debtor.objects.create(
            id               = 1,
            name             = '안당하',
            birth_date       = '2000-09-10'
        )
        Debtor.objects.create(
            id               = 2,
            name             = '이하서',
            birth_date       = '1972-07-11'
        )
        CreditScore.objects.create(
            id               = 1,
            score            = '627',
            credit_date      = '2020-07-31',
            debtor_id        = 1
        )
        CreditScore.objects.create(
            id               = 2,
            score            = '711',
            credit_date      = '2020-07-31',
            debtor_id        = 2
        ) 
        Deal.objects.create(
            id                  = 1,
            name                = '대환대출',
            earning_rate        = '10.00',
            interest_rate       =  3,
            repayment_period    = '12',
            net_amount          = '5100000',
            repayment_day       = '25',
            start_date          = '2020-06-15',
            end_date            = '2020-07-30',
            reason              = '타기관 대출 상환',
            category        = 1,
            status    = 1,
            debtor_id           = 1,
            grade           = 1,
            repayment_method = 1
        )
        Deal.objects.create(
            id                  = 2,
            name                = '대환대출',
            earning_rate        = '15.92',
            interest_rate       =  3,
            repayment_period    = '12',
            net_amount          = '6670000',
            repayment_day       = '25',
            start_date          = '2020-06-15',
            end_date            = '2020-07-30',
            reason              = '타기관 대출 상환',
            category        = 2,
            status      = 2,
            debtor_id           = 2,
            grade           = 2,
            repayment_method= 2
        )
        Mortgage.objects.create(
            id                        = 1,
            deal_id                   = 1, 
            latitude                  = '37.846111',
            longitude                 = '126.987581',
            estimated_recovery        = '1123200000',
            appraised_value           = '1021000000',
            senior_loan_amount        = '233510000',
            address                   = '경기 양주시 광적면 덕도리 86',
            completed_date            = '2020-06-09',
            scale                     = '175세대 / 9개동',
            supply_area               = '146.26',
            using_area                = '110.74',
            floors                    = '9층 / 15층',
            is_usage                  = False,
            selling_point_title       = '신축 브랜드 아파트',
            selling_point_description = '2020년 준공된 신축 브랜드 아파트입니다.'
        )
        MortgageImage.objects.create(
            id = 1,
            mortgage_id = 1,
            image_url = 'https://naver.com'
        )

    def test_deal_detail_category_1_success(self):
        client   = Client()
        response = client.get('/deals/1')
        self.assertEqual(response.json(),
        {
            "dealInfo": [
                {
                    "name"           : "대환대출",
                    "category"       : "부동산 담보대출",
                    "grade"          : "A+",
                    "earningRate"    : "10.00",
                    "repaymentPeriod": 12,
                    "repaymentMethod": "혼합",
                    "netAmount"      : 5100000,
                    "repaymentDay"   : 25,
                    "reason"         : "타기관 대출 상환",
                    "debtor"         : "안당하",
                    "creditScore"    : [
                        627,
                    ],
                    'amount' : 0,
                    'amountPercentage' : 0,
                    'investmentOption' : [5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000],
                }
            ],
            "mortgageInfo": [
                {
                    "latitude"               : "37.846111",
                    "longitude"              : "126.987581",
                    "estimatedRecovery"      : 1123200000,
                    "appraisedValue"         : 1021000000,
                    "seniorLoanAmount"       : 233510000,
                    "address"                : "경기 양주시 광적면 덕도리 86",
                    "completedDate"          : "2020-06-09",
                    "scale"                  : "175세대 / 9개동",
                    "supplyArea"             : "146.26",
                    "usingArea"              : "110.74",
                    "floor"                  : "9층 / 15층",
                    "isUsage"                : False,
                    "sellingPointTitle"      : "신축 브랜드 아파트",
                    "sellingPointDescription": "2020년 준공된 신축 브랜드 아파트입니다.",
                    "mortgageImage"          : [
                            'https://naver.com'
                        ]
                }
            ]
        }
    )

    def test_deal_detail_category_2_success(self):
        client   = Client()
        response = client.get('/deals/2')
        self.assertEqual(response.json(),
        {
            "dealInfo": [
                {
                    "name"           : "대환대출",
                    "category"       : "개인신용",
                    "grade"          : "A",
                    "earningRate"    : "15.92",
                    "repaymentPeriod": 12,
                    "repaymentMethod": "원리금균등",
                    "netAmount"      : 6670000,
                    "repaymentDay"   : 25,
                    "reason"         : "타기관 대출 상환",
                    "debtor"         : "이하서",
                    "creditScore"    : [
                        711,
                    ],
                    'amount' : 0,
                    'amountPercentage' : 0,
                    'investmentOption' : [5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000],
                }
            ]
        }
    )

    def test_deal_detail_get_invaild_error(self):
        client   = Client()
        response = client.get('/deals/133')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_ERROR'
            }
        )

class DealTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Bank.objects.create(
            id   = 1,
            name = '신한은행'
        )

        User.objects.create(
            id                        = 1,
            email                     = 'testman@gmail.com',
            password                  = '1asdfkjadkf',
            name                      = '이준영',
            deposit_amount            = 1000000,
            deposit_account           = '10202309432933',
            deposit_bank_id           = 1,
            withdrawal_account        = '123423531311433',
            withdrawal_bank_id        = 1,
            net_invest_limit          = 12313123,
            net_mortgage_invest_limit = 123214,
            credit_invest_limit       = 2000,
            is_activate               = True
        )

        Debtor.objects.create(
            id         = 1,
            name       = 'tester',
            birth_date = '2020-01-01'
        )
        
        Debtor.objects.create(
            id         = 2,
            name       = 'tester',
            birth_date = '2020-01-01'
        )

        Debtor.objects.create(
            id         = 3,
            name       = 'tester',
            birth_date = '2020-01-01'
        )

        Debtor.objects.create(
            id         = 4,
            name       = 'tester',
            birth_date = '2020-01-01'
        )

        Debtor.objects.create(
            id         = 5,
            name       = 'tester',
            birth_date = '2020-01-01'
        )

        Debtor.objects.create(
            id         = 6,
            name       = 'tester',
            birth_date = '2020-01-01'
        )

        Debtor.objects.create(
            id         = 7,
            name       = '아이유',
            birth_date = '2020-01-01'
        )

        Deal.objects.create(
            id                  = 1,
            name                = '송도아파트',
            category            = 1,
            grade               = 2,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2021-06-30',
            end_date            = '2021-07-30',
            reason              = '아이스크림',
            debtor_id           = 1,
            status              = 1
        )
        
        Deal.objects.create(
            id                  = 2,
            name                = '롯데아파트',
            category            = 1,
            grade               = 2,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2021-06-30',
            end_date            = '2021-07-30',
            reason              = '아이스크림',
            debtor_id           = 2,
            status              = 1
        )

        Deal.objects.create(
            id                  = 3,
            name                = '인천아파트',
            category            = 1,
            grade               = 1,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2020-06-30',
            end_date            = '2020-07-30',
            reason              = '에어컨 구매',
            debtor_id           = 3,
            status              = 1
        )

        Deal.objects.create(
            id                  = 4,
            name                = '군포아파트',
            category            = 1,
            grade               = 3,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 2,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2022-06-30',
            end_date            = '2022-07-30',
            reason              = '선풍기 구매',
            debtor_id           = 4,
            status              = 8
        )

        Deal.objects.create(
            id                  = 5,
            name                = '서울아파트',
            category            = 1,
            grade               = 1,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2021-06-30',
            end_date            = '2021-07-30',
            reason              = '선풍기구매',
            debtor_id           = 5,
            status              = 1
        )

        Deal.objects.create(
            id                  = 6,
            name                = '선릉아파트',
            category            = 1,
            grade               = 1,
            earning_rate        = 8.14,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 9000000,
            repayment_day       = 25,
            start_date          = '2021-06-30',
            end_date            = '2021-07-30',
            reason              = '대환대출',
            debtor_id           = 6,
            status              = 1
        )

        Deal.objects.create(
            id                  = 7,
            name                = '대환대출',
            category            = 2,
            grade               = 1,
            earning_rate        = 10,
            interest_rate       = 3.24,
            repayment_period    = 12,
            repayment_method    = 1,
            net_amount          = 10000000,
            repayment_day       = 25,
            start_date          = '2021-06-30',
            end_date            = '2021-07-30',
            reason              = '대환대출',
            debtor_id           = 7,
            status              = 1
        )

        Mortgage.objects.create(
            id                        = 1,
            deal_id                   = 1,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 중구',
            completed_date            = '2019-04-04',
            scale                     = '1548가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '20층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )

        Mortgage.objects.create(
            id                        = 2,
            deal_id                   = 2,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 십구',
            completed_date            = '2019-04-04',
            scale                     = '1548가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '20층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )

        Mortgage.objects.create(
            id                        = 3,
            deal_id                   = 3,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 백구',
            completed_date            = '2019-04-04',
            scale                     = '154가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '20층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )

        Mortgage.objects.create(
            id                        = 4,
            deal_id                   = 4,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 천구',
            completed_date            = '2019-04-04',
            scale                     = '548가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '20층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )

        Mortgage.objects.create(
            id                        = 5,
            deal_id                   = 5,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 만구',
            completed_date            = '2019-04-04',
            scale                     = '148가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '20층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )

        Mortgage.objects.create(
            id                        = 6,
            deal_id                   = 6,
            latitude                  = 38.123454,
            longitude                 = 133.123456,
            estimated_recovery        = 123,
            appraised_value           = 1000000000,
            senior_loan_amount        = 100000000,
            address                   = '서울시 귀엽구',
            completed_date            = '2019-04-04',
            scale                     = '154가구',
            supply_area               = 32.32,
            using_area                = 13.13,
            floors                    = '2층',
            is_usage                  = True,
            selling_point_title       = 'legeno',
            selling_point_description = 'real_legeno'
        )
        
        MortgageImage.objects.create(
            id          = 1,
            mortgage_id = 1,
            image_url   = 'www.naver.com'
        )

        MortgageImage.objects.create(
            id          = 2,
            mortgage_id = 1,
            image_url   = 'www.naver1.com'
        )

        MortgageImage.objects.create(
            id          = 3,
            mortgage_id = 2,
            image_url   = 'www.naver2.com'
        )

        MortgageImage.objects.create(
            id          = 4,
            mortgage_id = 2,
            image_url   = 'www.naver3.com'
        )

        MortgageImage.objects.create(
            id          = 5,
            mortgage_id = 3,
            image_url   = 'www.naver4.com'
        )

        MortgageImage.objects.create(
            id          = 6,
            mortgage_id = 3,
            image_url   = 'www.naver5.com'
        )

        MortgageImage.objects.create(
            id          = 7,
            mortgage_id = 4,
            image_url   = 'www.naver6.com'
        )

        MortgageImage.objects.create(
            id          = 8,
            mortgage_id = 4,
            image_url   = 'www.naver7.com'
        )

        MortgageImage.objects.create(
            id          = 9,
            mortgage_id = 5,
            image_url   = 'www.naver8.com'
        )

        MortgageImage.objects.create(
            id          = 10,
            mortgage_id = 5,
            image_url   = 'www.naver9.com'
        )

        MortgageImage.objects.create(
            id          = 11,
            mortgage_id = 6,
            image_url   = 'www.naver10.com'
        )

        MortgageImage.objects.create(
            id          = 12,
            mortgage_id = 6,
            image_url   = 'www.naver11.com'
        )

        UserDeal.objects.create(
            id      = 1,
            user_id = 1,
            deal_id = 1,
            amount  = 900000
        )

        UserDeal.objects.create(
            id      = 2,
            user_id = 1,
            deal_id = 2,
            amount  = 1800000
        )

        UserDeal.objects.create(
            id      = 3,
            user_id = 1,
            deal_id = 5,
            amount  = 450000
        )

        UserDeal.objects.create(
            id      = 4,
            user_id = 1,
            deal_id = 6,
            amount  = 900000
        )

        UserDeal.objects.create(
            id      = 5,
            user_id = 1,
            deal_id = 3,
            amount  = 9000000
        )

        UserDeal.objects.create(
            id      = 7,
            user_id = 1,
            deal_id = 7,
            amount  = 100000
        )
        
    
    def test_mortgage_dealview_get_success(self):
        client   = Client()
        response = client.get('/deals?category=mortgage')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "recruitingResults" : [
                    {
                        "index"           : 1,
                        "title"           : "송도아파트",
                        "grade"           : "A",
                        "period"          : 12,
                        "earningRate"     : "8.14",
                        "amount"          : 9000000,
                        "titleImage"      : "www.naver.com",
                        "startDate"       : "2021-06-30",
                        "progress"        : 10,
                        "investmentAmount": 900000
                    },
                    {
                        "index"           : 2,
                        "title"           : "롯데아파트",
                        "grade"           : "A",
                        "period"          : 12,
                        "earningRate"     : "8.14",
                        "amount"          : 9000000,
                        "titleImage"      : "www.naver2.com",
                        "startDate"       : "2021-06-30",
                        "progress"        : 20,
                        "investmentAmount": 1800000
                    },
                    {
                        "index"           : 5,
                        "title"           : "서울아파트",
                        "grade"           : "A+",
                        "period"          : 12,
                        "earningRate"     : "8.14",
                        "amount"          : 9000000,
                        "titleImage"      : "www.naver8.com",
                        "startDate"       : "2021-06-30",
                        "progress"        : 5,
                        "investmentAmount": 450000
                    },
                    {
                        "index"           : 6,
                        "title"           : "선릉아파트",
                        "grade"           : "A+",
                        "period"          : 12,
                        "earningRate"     : "8.14",
                        "amount"          : 9000000,
                        "titleImage"      : "www.naver10.com",
                        "startDate"       : "2021-06-30",
                        "progress"        : 10,
                        "investmentAmount": 900000
                    }
                ],
                "scheduledResults" : [
                    {
                        "index"      : 4,
                        "title"      : "군포아파트",
                        "period"     : 12,
                        "earningRate": "8.14",
                        "amount"     : 9000000,
                        "titleImage" : "www.naver6.com",
                        "startDate"  : "2022-06-30"
                    }
                ]
            }
        )
    
    def test_closed_mortgage_dealview_get_success(self):
        client   = Client()
        response = client.get('/deals?category=mortgage&closed=true&offset=0&limit=12')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "count" : 1,
                "results" : [
                    {
                        "index"           : 3,
                        "title"           : "인천아파트",
                        "grade"           : "A+",
                        "period"          : 12,
                        "earningRate"     : "8.14",
                        "amount"          : 9000000,
                        "titleImage"      : "www.naver4.com",
                        "startDate"       : "2020-06-30",
                        "progress"        : 100,
                        "investmentAmount": 9000000
                    }
                ]
            }
        )

    def test_individual_dealview_get_success(self):
        client   = Client()
        response = client.get('/deals?category=individual')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "count" : 1,
                "results" : [
                    {
                        "index"           : 7,
                        "title"           : "대환대출",
                        "grade"           : "A+",
                        "period"          : 12,
                        "earningRate"     : "10.00",
                        "amount"          : 10000000,
                        "titleImage"      : None,
                        "startDate"       : "2021-06-30",
                        "progress"        : 1,
                        "investmentAmount": 100000
                    }
                ]
            }
        )

    def test_dealview_get_value_error(self):
        client   = Client()
        response = client.get('/deals?category=mortgage&closed=true&offset=0&limit=1!')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'VALUE_ERROR'
            }
        )

    def test_dealview_get_invaild_input(self):
        client   = Client()
        response = client.get('/deals?category=mrtgage&closed=true&offset=0&limit=12')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_INPUT'
            }
        )

class LoanAmountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        Bank.objects.create(
            id   = 1,
            name = "농협은행"
        )

        TOTAL_USER   = 1
        TOTAL_DEBTOR = 10
        TOTAL_DEAL   = 10

        User.objects.create(
            id             = 1,
            email           = "example@gmail.com",
            password        = 12345645489,
            deposit_bank_id = 1,
            deposit_account = "12344567",
            deposit_amount  = 5000
        )

        for i in range(1, TOTAL_DEBTOR + 1):
            Debtor.objects.create(
                id         = i,
                name       = f"채무자_{i}",
                birth_date = "2020-01-01"
            )

        userdeal_id    = 1
        userpayback_id = 1
        today          = datetime.today().date()
        delay_day      = today - timedelta(days=30)
        overdue_day    = today - timedelta(days=90)
        nonperform_day = today - timedelta(days=150)
        for i in range(1, TOTAL_DEAL + 1):
            if i % 2== 0:
                deal_status = Deal.Status.NORMAL_COMPLETION.value
            elif i % 3 == 0:
                deal_status = Deal.Status.NORMAL.value
            else:
                deal_status = ((i+1)//2) % 8 + 1
            deal_repayment_method         = i % 4 + 1
            deal_category                 = i % 5 + 1
            deal_grade                    = i % 12 + 1
            deal_amount                   = (i % 50 + 1) * 120000
            deal_interest_rate_per_month  = (i % 12 + 5) / 100 / 12
            deal_repayment_period         = 12
            deal_repayment_day            = i % 25 + 1

            userdeal_total_principal = deal_amount // TOTAL_USER
            # Calculate Start Date & End Date by Deal Status
            if deal_status == Deal.Status.SCHEDULED.value:
                delta_day = -10

            elif deal_status == Deal.Status.APPLYING.value:
                delta_day = 10
                userdeal_total_principal *= 0.5

            elif deal_status == Deal.Status.NORMAL_COMPLETION.value or \
                deal_status == Deal.Status.NONPERFORM_COMPLETION.value:
                delta_day = 600

            else:
                delta_day = (10 * i) % 300 + 60

            start_date = today - timedelta(days=delta_day)
            end_date   = start_date + timedelta(days=30)

            # Calculate total_amount_per_month by Deal Repayment Method
            if deal_repayment_method == Deal.RepaymentMethod.MIX.value:
                total_amount_per_month = userdeal_total_principal / 20

            elif deal_repayment_method == Deal.RepaymentMethod.EQUAL_SUM.value:
                tmp = (1 + deal_interest_rate_per_month) ** deal_repayment_period
                total_amount_per_month = userdeal_total_principal * deal_interest_rate_per_month * tmp / (tmp - 1)

            # Calculate Deal Earning Rate  
            if deal_repayment_method == Deal.RepaymentMethod.MIX.value or \
                deal_repayment_method == Deal.RepaymentMethod.EQUAL_SUM.value:
                interest = 0
                left_principal = userdeal_total_principal
                for _ in range(deal_repayment_period):
                    interest       += left_principal * deal_interest_rate_per_month
                    left_principal -= (total_amount_per_month - interest)

                deal_earning_rate = interest / userdeal_total_principal * 100

            elif deal_repayment_method == Deal.RepaymentMethod.MATURE.value:
                deal_earning_rate = deal_interest_rate_per_month * 12 * 100

            elif deal_repayment_method == Deal.RepaymentMethod.EQUAL_PRINCIPAL.value:
                deal_earning_rate = (deal_repayment_period + 1) / 2 * deal_interest_rate_per_month

            Deal.objects.create(
                id               = i,
                name             = f"deal_{i}",
                category         = deal_category,
                grade            = deal_grade,
                earning_rate     = deal_earning_rate,
                interest_rate    = deal_interest_rate_per_month * 12,
                repayment_period = deal_repayment_period,
                repayment_method = deal_repayment_method,
                net_amount       = deal_amount,
                repayment_day    = deal_repayment_day,
                start_date       = start_date,
                end_date         = end_date,
                reason           = f"reason_{i}",
                debtor_id        = i % TOTAL_DEBTOR + 1,
                status           = deal_status
            )

            if deal_category == 1:
                Mortgage.objects.create(
                    id                        = i // 5 + 1,
                    deal_id                   = i,
                    latitude                  = 11.111111,
                    longitude                 = 22.222222,
                    estimated_recovery        = 1200000000,
                    appraised_value           = 1000000000,
                    senior_loan_amount        = 200000000,
                    address                   = f"address_{i//5+1}",
                    completed_date            = '2020-01-01',
                    scale                     = 'scale',
                    supply_area               = 30.00,
                    using_area                = 25.00,
                    floors                    = 'floors',
                    is_usage                  = i % 2,
                    selling_point_title       = 'selling_point_title',
                    selling_point_description = 'selling_point_description'
                )

                MortgageImage.objects.create(
                    id = i // 5 + 1,
                    mortgage_id = i // 5 + 1,
                    image_url   = "mortgage_image_url"
                )

            if deal_status == Deal.Status.SCHEDULED.value:
                continue

            for j in range(1, TOTAL_USER + 1):
                UserDeal.objects.create(
                    id      = userdeal_id,
                    user_id = j,
                    deal_id = i,
                    amount  = userdeal_total_principal
                )

                payback_date   = end_date.replace(day=1) + timedelta(days=32)
                payback_date   = datetime(payback_date.year, payback_date.month, deal_repayment_day).date()
                left_principal = userdeal_total_principal

                if deal_repayment_method == Deal.RepaymentMethod.MATURE.value:
                    principal = 0
                elif deal_repayment_method == Deal.RepaymentMethod.EQUAL_PRINCIPAL.value:
                    principal = userdeal_total_principal // deal_repayment_period

                for k in range(1, deal_repayment_period + 1):
                    interest = round(left_principal * deal_interest_rate_per_month)

                    if deal_repayment_method == Deal.RepaymentMethod.MIX.value or \
                        deal_repayment_method == Deal.RepaymentMethod.EQUAL_SUM.value:
                        principal = int(total_amount_per_month - interest)

                    state = UserPayback.State.PAID.value
                    if deal_status == Deal.Status.DELAY.value:
                        if delay_day < payback_date <= today:
                            state = UserPayback.State.UNPAID.value
                    elif deal_status == Deal.Status.OVERDUE.value:
                        if overdue_day < payback_date <= today:
                            state = UserPayback.State.UNPAID.value
                    elif deal_status == Deal.Status.NONPERFORM.value:
                        if nonperform_day < payback_date <= today:
                            state = UserPayback.State.UNPAID.value
                    elif deal_status == Deal.Status.NONPERFORM_COMPLETION.value:
                        if payback_date > end_date + timedelta(days=200):
                            state = UserPayback.State.UNPAID.value

                    UserPayback.objects.create(
                        id             = userpayback_id,
                        users_deals_id = userdeal_id,
                        interest       = interest,
                        principal      = principal if k < deal_repayment_period else left_principal,
                        tax            = ((interest * 0.15) // 10) * 10,
                        commission     = int(interest * 0.15),
                        payback_round  = k,
                        payback_date   = payback_date,
                        state          = UserPayback.State.TOBE_PAID.value if today < payback_date else state
                    )

                    userpayback_id += 1
                    payback_date    = payback_date.replace(day=1) + timedelta(days=32)
                    payback_date    = datetime(payback_date.year, payback_date.month, deal_repayment_day).date()
                    left_principal -= principal

                userdeal_id += 1
    def test_closed_mortgage_dealview_get_success(self):
        client   = Client()
        response = client.get('/deals/loan-amount')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'result': {
                    'avgPerPerson': 7800000, 
                    'investAcc': 10, 
                    'loanAcc': 7800000
                }
            }
        )