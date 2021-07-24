import json
import unittest
import bcrypt, jwt
from datetime   import datetime, timedelta

from django.test import TestCase, Client

from users.models       import Bank, User
from deals.models       import Debtor, Deal, Mortgage, MortgageImage
from investments.models import UserDeal, UserPayback
from my_settings        import SECRET_KEY, ALGORITHM

class InvestmentsSummaryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Bank.objects.create(
            id   = 1,
            name = "농협은행"
        )

        TOTAL_USER   = 1
        TOTAL_DEBTOR = 10
        TOTAL_DEAL   = 10

        hashed_password = bcrypt.hashpw("P@ssword".encode('utf-8'), bcrypt.gensalt())
        User.objects.create(
            id             = 1,
            email           = "example@gmail.com",
            password        = hashed_password.decode(),
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

    def test_investments_history_view_success(self):
        client = Client()

        access_token = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_AUTHORIZATION': access_token}
        response     = client.get("/investments/history", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                "summary": {
                    "total":7800000,
                    "paidTotal":4681044,
                    "paidInterest":522414
                },
                "count": {
                    "all":10,
                    "1":0,
                    "2":3,
                    "3":0,
                    "4":1,
                    "5":1,
                    "6":5,
                    "7":0,
                    "8":0
                },
                "items": [
                    {
                        "id":10,
                        "dealIndex":10,
                        "item":"deal_10",
                        "amount":1320000,
                        "principal":1320000,
                        "interest":198000,
                        "date":"21.07.27",
                        "grade":"D",
                        "interestRate":"15.00",
                        "term":12,
                        "status":6,
                        "repayment":100,
                        "cycle":12,
                        "isCancelable":False
                    },
                    {
                        "id":9,
                        "dealIndex":9,
                        "item":"deal_9",
                        "amount":1200000,
                        "principal":1200000,
                        "interest":92937,
                        "date":"21.07.27",
                        "grade":"D+",
                        "interestRate":"10.39",
                        "term":12,
                        "status":2,
                        "repayment":31,
                        "cycle":4,
                        "isCancelable":False
                    },
                    {
                        "id":8,
                        "dealIndex":8,
                        "item":"deal_8",
                        "amount":1080000,
                        "principal":1080000,
                        "interest":109037,
                        "date":"21.07.27",
                        "grade":"C-",
                        "interestRate":"12.61",
                        "term":12,
                        "status":6,
                        "repayment":100,
                        "cycle":12,
                        "isCancelable":False
                    },
                    {
                        "id":7,
                        "dealIndex":7,
                        "item":"deal_7",
                        "amount":960000,
                        "principal":960000,
                        "interest":62400,
                        "date":"21.07.27",
                        "grade":"C",
                        "interestRate":"0.07",
                        "term":12,
                        "status":5,
                        "repayment":0,
                        "cycle":0,
                        "isCancelable":False
                    },
                    {
                        "id":6,
                        "dealIndex":6,
                        "item":"deal_6",
                        "amount":840000,
                        "principal":840000,
                        "interest":92400,
                        "date":"21.07.27",
                        "grade":"C+",
                        "interestRate":"11.00",
                        "term":12,
                        "status":6,
                        "repayment":100,
                        "cycle":12,
                        "isCancelable":False
                    },
                    {
                        "id":5,
                        "dealIndex":5,
                        "item":"deal_5",
                        "amount":720000,
                        "principal":720000,
                        "interest":39595,
                        "date":"21.07.27",
                        "grade":"B-",
                        "interestRate":"6.82",
                        "term":12,
                        "status":4,
                        "repayment":0,
                        "cycle":0,
                        "isCancelable":False
                    },
                    {
                        "id":4,
                        "dealIndex":4,
                        "item":"deal_4",
                        "amount":600000,
                        "principal":600000,
                        "interest":41057,
                        "date":"21.07.27",
                        "grade":"B",
                        "interestRate":"8.01",
                        "term":12,
                        "status":6,
                        "repayment":100,
                        "cycle":12,
                        "isCancelable":False
                    },
                    {
                        "id":3,
                        "dealIndex":3,
                        "item":"deal_3",
                        "amount":480000,
                        "principal":480000,
                        "interest":20800,
                        "date":"21.07.27",
                        "grade":"B+",
                        "interestRate":"0.04",
                        "term":12,
                        "status":2,
                        "repayment":16,
                        "cycle":2,
                        "isCancelable":False
                    },
                    {
                        "id":2,
                        "dealIndex":2,
                        "item":"deal_2",
                        "amount":360000,
                        "principal":360000,
                        "interest":25200,
                        "date":"21.07.27",
                        "grade":"A-",
                        "interestRate":"7.00",
                        "term":12,
                        "status":6,
                        "repayment":100,
                        "cycle":12,
                        "isCancelable":False
                    },
                    {
                        "id":1,
                        "dealIndex":1,
                        "item":"deal_1",
                        "amount":240000,
                        "principal":240000,
                        "interest":7873,
                        "date":"21.07.27",
                        "grade":"A",
                        "interestRate":"3.74",
                        "term":12,
                        "status":2,
                        "repayment":8,
                        "cycle":1,
                        "isCancelable":False
                    }
                ]
            }
        )

    def test_investments_history_search_view_success(self):
        client = Client()

        access_token = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_AUTHORIZATION': access_token}
        response     = client.get("/investments/history?search=3&offset=0&limit=10", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                    {
                "summary":{
                    "total":480000,
                    "paidTotal":80000,
                    "paidInterest":6133
                },
                "count":{
                    "all":10,
                    "1":0,
                    "2":3,
                    "3":0,
                    "4":1,
                    "5":1,
                    "6":5,
                    "7":0,
                    "8":0
                },
                "items":[
                    {
                        "id":3,
                        "dealIndex":3,
                        "item":"deal_3",
                        "amount":480000,
                        "principal":480000,
                        "interest":20800,
                        "date":"21.07.27",
                        "grade":"B+",
                        "interestRate":"0.04",
                        "term":12,
                        "status":2,
                        "repayment":16,
                        "cycle":2,
                        "isCancelable":False
                    }
                ]
            }
        )

    def test_investment_history_get_value_error(self):
        client   = Client()
        access_token = jwt.encode({"user_id": 1}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_AUTHORIZATION': access_token}
        response     = client.get("/investments/history?search=개인&offset=0&limit=10!", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'VALUE_ERROR'
            }
        )