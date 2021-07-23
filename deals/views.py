import json
from django.db.models.aggregates import Sum
from django.views     import View
from django.http      import JsonResponse
from deals.models        import Deal, Debtor, Mortgage, MortgageImage, CreditScore
from investments.models  import UserDeal

class DealDetailView(View):
    def get(self, request, deal_id):
        try:
            deal = Deal.objects.get(id=deal_id)
            deal_info = [{
                "name"            : deal.name,
                "category"        : Deal.Category(deal.category).label,
                "grade"           : Deal.Grade(deal.grade).label,
                "earningRate"     : deal.earning_rate,
                "repaymentPeriod" : deal.repayment_period,
                "repaymentMethod" : Deal.RepaymentMethod(deal.repayment_method).label,
                "netAmount"       : deal.net_amount,
                "repaymentDay"    : deal.repayment_day,
                "reason"          : deal.reason,
                "debtor"          : deal.debtor.name,
                "creditScore"     : [score.score for score in deal.debtor.creditscore_set.all()],
                "amount"          : deal.userdeal_set.aggregate(total_price=Sum('amount'))['total_price'] or 0,
                "amountPercentage": int((deal.userdeal_set.aggregate(total_price=Sum('amount'))['total_price'] or 0)/deal.net_amount)*100,
                "investmentOption": [5000,10000,20000,50000,100000,200000,300000,400000,500000,1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,5000000,6000000,7000000,8000000,9000000,10000000]
            }]
            if Deal.Category(deal.category).label == '부동산 담보대출': 
                mortgage = Mortgage.objects.get(deal=deal)
                mortgage_info = [{
                    "latitude"                : mortgage.latitude,
                    "longitude"               : mortgage.longitude,
                    "estimatedRecovery"       : mortgage.estimated_recovery,
                    "appraisedValue"          : mortgage.appraised_value,
                    "seniorLoanAmount"        : mortgage.senior_loan_amount,
                    "address"                 : mortgage.address,
                    "completedDate"           : mortgage.completed_date,
                    "scale"                   : mortgage.scale,
                    "supplyArea"              : mortgage.supply_area,
                    "usingArea"               : mortgage.using_area,
                    "floor"                   : mortgage.floors,
                    "isUsage"                 : mortgage.is_usage,
                    "sellingPointTitle"       : mortgage.selling_point_title,
                    "sellingPointDescription" : mortgage.selling_point_description,
                    "mortgageImage"           : [image.image_url for image in mortgage.mortgageimage_set.all()]
                }]
                return JsonResponse({"dealInfo":deal_info,"mortgageInfo":mortgage_info}, status=200)
            return JsonResponse({"dealInfo":deal_info}, status=200)
        except Deal.DoesNotExist:
            return JsonResponse({"message":"INVALID_ERROR"}, status=400)