from deals.models   import Deal

class Portfolio:
    def __init__(self):
        self.grade = {
            'grades'  : ['a', 'b', 'c', 'd', 'etc'],
            'amounts' : [0, 0, 0, 0, 0],
            'counts'  : [0, 0, 0, 0, 0]
        }
        
        self.earning_rate = {
            'earningRates' : ["underEight", "overEight", "overTen", "overTwelve"],
            'amounts'      : [0, 0, 0, 0],
            'counts'       : [0, 0, 0, 0]
        }

        self.category = {
            "categories" : ["personal", "company", "special", "estate", "etc"],
            'amounts'    : [0, 0, 0, 0, 0],
            'counts'     : [0, 0, 0, 0, 0]
        }

    def sort_deal(self, user_deal):
        self._set_by_grade(user_deal)
        self._set_by_earning_rate(user_deal)
        self._set_by_categry(user_deal)

    def _set_by_grade(self, user_deal):
        grade = user_deal.deal.grade

        if grade in [Deal.Grade.A_PLUS.value, Deal.Grade.A.value, Deal.Grade.A_MINUS.value]:
            index = 0

        elif grade in [Deal.Grade.B_PLUS.value, Deal.Grade.B.value, Deal.Grade.B_MINUS.value]:
            index = 1

        elif grade in [Deal.Grade.C_PLUS.value, Deal.Grade.C.value, Deal.Grade.C_MINUS.value]:
            index = 2

        elif grade in [Deal.Grade.D_PLUS.value, Deal.Grade.D.value, Deal.Grade.D_MINUS.value]:
            index = 3

        else:
            index = 4

        self.grade['amounts'][index] += user_deal.amount
        self.grade['counts'][index]  += 1


    def _set_by_earning_rate(self, user_deal):
        earning_rate = user_deal.deal.earning_rate

        if earning_rate < 8:
            index = 0

        elif earning_rate < 10:
            index = 1

        elif earning_rate < 12:
            index = 2

        else:
            index = 3
        
        self.earning_rate['amounts'][index] += user_deal.amount
        self.earning_rate['counts'][index]  += 1


    def _set_by_categry(self, user_deal):
        category = user_deal.deal.category

        if category == Deal.Category.CREDIT.value:
            index = 0

        elif category == Deal.Category.COMPANY.value:
            index = 1

        elif category == Deal.Category.SPECIAL.value:
            index = 2

        elif category == Deal.Category.MORTGAGE.value:
            index = 3

        else:
            index = 4

        self.category['amounts'][index] += user_deal.amount
        self.category['counts'][index]  += 1
