from django.test  import TestCase, Client

from deals.models import CreditScore, Deal, Debtor, Mortgage, MortgageImage

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