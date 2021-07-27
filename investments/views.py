import json
from datetime   import datetime, timedelta

from django.views     import View
from django.http      import JsonResponse
from django.utils     import timezone
from django.db.models import Sum, Q, Prefetch
from django.db        import transaction

from users.utils        import user_validator
from investments.models import PaybackSchedule, UserDeal, UserPayback
from deals.models       import Deal

class InvestmentHistoryView(View):
    @user_validator
    def get(self, request):
        try:
            signed_user = request.user
            PAGE_SIZE   = 10
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', PAGE_SIZE)) + offset
            status      = request.GET.get('status', None)
            search      = request.GET.get('search', None)
            user_deals  = UserDeal.objects.filter(user=signed_user).select_related('deal')
            q           = Q()

            count_by_status = {"all": len(user_deals)}

            for deal_status in Deal.Status.__members__:
                count_by_status[Deal.Status[deal_status]] = len(user_deals.filter(deal__status=Deal.Status[deal_status]))

            if status:
                q &= Q(deal__status=status)

            if search:
                q &= Q(deal__name__contains=search) | Q(deal__id__contains=search)

            investments  = user_deals.filter(q).prefetch_related(
                Prefetch('userpayback_set', to_attr='paybacks'),
                Prefetch('userpayback_set', queryset=UserPayback.objects.filter(state=UserPayback.State.PAID.value), to_attr='paid_paybacks')
                )

            summary = {
                "total"       : sum(investment.amount for investment in investments),
                "paidTotal"   : investments.filter(userpayback__state=UserPayback.State.PAID.value)\
                                .aggregate(paid_total=Sum('userpayback__principal'))['paid_total'],
                "paidInterest": investments.filter(userpayback__state=UserPayback.State.PAID.value)\
                                .aggregate(paid_interest=Sum('userpayback__interest'))['paid_interest']
            }

            items = [
                {
                    "id"          : investment.id,
                    "dealIndex"   : investment.deal.id,
                    "item"        : investment.deal.name,
                    "amount"      : investment.amount,
                    "principal"   : sum(payback.principal for payback in investment.paybacks),
                    "interest"    : sum(payback.interest for payback in investment.paybacks),
                    "date"        : timezone.localtime(investment.created_at).strftime("%y.%m.%d"),
                    "grade"       : Deal.Grade(investment.deal.grade).label,
                    "interestRate": investment.deal.earning_rate,
                    "term"        : investment.deal.repayment_period,
                    "status"      : investment.deal.status,
                    "repayment"   : int((sum(paid_payback.principal for paid_payback in investment.paid_paybacks) / investment.amount) * 100),
                    "cycle"       : len(investment.paid_paybacks),
                    "isCancelable": investment.created_at + timezone.timedelta(days=1) < timezone.now(),
                } for investment in investments.order_by('-created_at')[offset:limit]
            ]
            return JsonResponse({"summary":summary,"count": count_by_status, "items":items}, status=200)

        except ValueError:
            return JsonResponse({"message":'VALUE_ERROR'}, status=400)

class InvestDealView(View):
    @user_validator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            with transaction.atomic():
                for investment in data['investments']:
                    deal = Deal.objects.get(id=investment['id'])

                    userdeal = UserDeal.objects.create(
                        user   = user,
                        deal   = deal,
                        amount = investment['amount']
                    )
                    
                    paybacks = PaybackSchedule.objects.filter(deal=deal, principal=investment['amount'])

                    for payback in PaybackSchedule.objects.all():
                        print(payback.principal)

                    for payback in paybacks:
                        userpayback = UserPayback.objects.create(
                            user_deals    = userdeal,
                            principal     = payback.principal,
                            interest      = payback.interest,
                            tax           = payback.tax,
                            commission    = payback.commission,
                            payback_round = payback.round,
                            payback_date  = payback.date,
                            state         = UserPayback.State.TOBE_PAID.value,
                        )
                        print("$#^%@@#%@#$%@#$")
                        print(userpayback.values())

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
