import math

from django.db.models import Sum, Prefetch, Q, F
from django.views     import View
from django.http      import JsonResponse
from django.utils     import timezone

from deals.models       import Deal, Mortgage, MortgageImage

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

class DealsView(View):
    def get(self, request):
        try:
            deal_closed = request.GET.get('closed', False)
            category    = request.GET.get('category', False)
            PAGE_SIZE   = 12
            q           = Q()
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', PAGE_SIZE)) + offset

            categories = {
                'mortgage'  : Deal.Category.MORTGAGE.value,
                'individual': Deal.Category.CREDIT.value
            }

            if category not in categories:
                return JsonResponse({"message":"INVALID_INPUT"}, status=400)

            q.add(Q(category=categories[category]), q.AND)
            
            if deal_closed == 'true' and categories[category] == Deal.Category.MORTGAGE.value:
                q.add(Q(end_date__lt=timezone.localdate()) | Q(net_reservation=F('net_amount')), q.AND)

            else:
                limit  = None
                q.add(Q(end_date__gte=timezone.localdate()) & Q(start_date__lte=timezone.localdate()), q.AND)

            deals = Deal.objects.annotate(net_reservation=Sum('userdeal__amount')).filter(q).prefetch_related(
                Prefetch(
                    'mortgage_set', 
                    queryset=Mortgage.objects.prefetch_related(
                        Prefetch(
                            'mortgageimage_set', 
                            queryset=MortgageImage.objects.all(), 
                            to_attr='image')
                            ), to_attr='mortgages'))

            results = [
                {
                    'index'           : deal.id,
                    'title'           : deal.name,
                    'grade'           : Deal.Grade(deal.grade).label,
                    'period'          : deal.repayment_period,
                    'earningRate'     : deal.earning_rate,
                    'amount'          : deal.net_amount,
                    'titleImage'      : deal.mortgages[0].image[0].image_url\
                                        if categories[category] == Deal.Category.MORTGAGE.value else None,
                    'startDate'       : deal.start_date,
                    'progress'        : math.trunc(((deal.net_reservation or 0) / deal.net_amount) * 100),
                    'investmentAmount': deal.net_reservation or 0
                } for deal in deals[offset:limit]
            ]

            if deal_closed != 'true' and categories[category] == Deal.Category.MORTGAGE.value:
                scheduled_results = [
                    {
                        'index'      : deal.id,
                        'title'      : deal.name,
                        'period'     : deal.repayment_period,
                        'earningRate': deal.earning_rate,
                        'amount'     : deal.net_amount,
                        'titleImage' : deal.mortgages[0].image[0].image_url,
                        'startDate'  : deal.start_date
                    } for deal in Deal.objects.filter(status=Deal.Status.SCHEDULED.value, category=Deal.Category.MORTGAGE.value).prefetch_related(
                Prefetch(
                    'mortgage_set', 
                    queryset=Mortgage.objects.prefetch_related(
                        Prefetch(
                            'mortgageimage_set', 
                            queryset=MortgageImage.objects.all(), 
                            to_attr='image')
                            ), to_attr='mortgages'))
                ]

                return JsonResponse({"recruitingResults": results, "scheduledResults": scheduled_results}, status=200)
            
            return JsonResponse({"results":results, "count":len(deals)}, status=200)

        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status=400)
