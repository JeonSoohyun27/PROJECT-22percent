import json
from datetime   import datetime, timedelta

from django.views     import View
from django.http      import JsonResponse
from django.utils     import timezone
from django.db.models import Sum, Q, Prefetch

from users.utils        import user_validator
from investments.utils  import Portfolio
from investments.models import UserDeal, UserPayback
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

class InvestmentPortfolioView(View):
    @user_validator
    def get(self, request):
        user = request.user

        user_deals = list(user.userdeal_set.all().prefetch_related('deal'))

        portfolio = Portfolio()

        for user_deal in user_deals:
            portfolio.sort_deal(user_deal)

        results = {
            'grade'       : portfolio.grade,
            'earningRate' : portfolio.earning_rate,
            'category'    : portfolio.category
        }
        
        return JsonResponse({"results": results}, status=200)

class InvestmentSummaryView(View):
    @user_validator
    def get(self, request):
        user = request.user
        
        user_deals_by_status = {}
        for deal_status in Deal.Status.__members__:
            user_deals_by_status[deal_status] = user.userdeal_set.filter(
                Q(deal__status = Deal.Status[deal_status])
            ).prefetch_related(
                Prefetch(
                    'userpayback_set',
                    queryset = UserPayback.objects.all(),
                    to_attr  = 'all_paybacks'
                ),
                Prefetch(
                    'userpayback_set',
                    queryset = UserPayback.objects.filter(state=UserPayback.State.PAID.value),
                    to_attr  = 'paid_paybacks'
                ),
            )

        user_deals_by_status_sums = {}
        for key, filtered_user_deals in user_deals_by_status.items():
            user_deals_by_status_sums[key] = {
                'total_amount'     : int(filtered_user_deals.aggregate(Sum('amount'))['amount__sum'] or 0),
                'total_interest'   : sum(sum(payback.interest for payback in user_deal.all_paybacks) for user_deal in filtered_user_deals),
                'total_commission' : sum(sum(payback.commission for payback in user_deal.all_paybacks) for user_deal in filtered_user_deals),
                'paid_principal'   : sum(sum(payback.principal for payback in user_deal.paid_paybacks) for user_deal in filtered_user_deals),
                'paid_interest'    : sum(sum(payback.interest for payback in user_deal.paid_paybacks) for user_deal in filtered_user_deals),
                'paid_commission'  : sum(sum(payback.commission for payback in user_deal.paid_paybacks) for user_deal in filtered_user_deals)
            }

        applying_invest_amount   = user_deals_by_status_sums['APPLYING']['total_amount'] - \
                                   user_deals_by_status_sums['APPLYING']['paid_principal']
        normal_invest_amount     = user_deals_by_status_sums['NORMAL']['total_amount'] - \
                                   user_deals_by_status_sums['NORMAL']['paid_principal']
        delay_invest_amount      = user_deals_by_status_sums['DELAY']['total_amount'] - \
                                   user_deals_by_status_sums['DELAY']['paid_principal']
        overdue_invest_amount    = user_deals_by_status_sums['OVERDUE']['total_amount'] - \
                                   user_deals_by_status_sums['OVERDUE']['paid_principal']
        nonperform_invest_amount = user_deals_by_status_sums['NONPERFORM']['total_amount'] - \
                                   user_deals_by_status_sums['NONPERFORM']['paid_principal']
        loss_amount              = user_deals_by_status_sums['NONPERFORM_COMPLETION']['total_amount'] - \
                                   user_deals_by_status_sums['NONPERFORM_COMPLETION']['paid_principal']

        invested_amount = sum(value['total_amount'] for value in user_deals_by_status_sums.values())
        complete_amount = sum(value['paid_principal'] for value in user_deals_by_status_sums.values())
        invest_amount   = applying_invest_amount + normal_invest_amount + delay_invest_amount + \
                          overdue_invest_amount + nonperform_invest_amount

        paid_revenue = sum(value['paid_interest'] for value in user_deals_by_status_sums.values()) - \
                       sum(value['paid_commission'] for value in user_deals_by_status_sums.values())

        total_revenue = sum(value['total_interest'] for value in user_deals_by_status_sums.values()) - \
                        sum(value['total_commission'] for value in user_deals_by_status_sums.values())
        
        mortgage_deals = user.userdeal_set.filter(
            Q(deal__category=Deal.Category.MORTGAGE.value)
        ).prefetch_related(
            Prefetch('userpayback_set', queryset=UserPayback.objects.filter(~Q(state=UserPayback.State.PAID.value)), to_attr='left_paybacks')
        )
        
        invest_mortgage_amount = sum(sum(payback.principal for payback in mortgage_deal.left_paybacks) for mortgage_deal in mortgage_deals)

        deposit = {
            'bank'    : user.deposit_bank.name,
            'account' : user.deposit_account,
            'balance' : user.deposit_amount
        }

        invest_limit = {
            'total'        : user.net_invest_limit,
            'remainTotal'  : user.net_invest_limit - invest_amount,
            'remainEstate' : user.net_mortgage_invest_limit - invest_mortgage_amount 
        }

        overview = {
            'earningRate' : round((total_revenue - loss_amount) / complete_amount * 100, 2),
            'asset'       : user.deposit_amount + invest_amount,
            'paidRevenue' : paid_revenue
        }

        invest_status = {
            'totalInvest' : invested_amount,
            'complete'    : complete_amount,
            'delay'       : delay_invest_amount,
            'invest'      : invest_amount,
            'loss'        : loss_amount,
            'normal'      : normal_invest_amount + applying_invest_amount,
            'overdue'     : overdue_invest_amount,
            'nonperform'  : nonperform_invest_amount
        }

        results = {
            'deposit'      : deposit,
            'investLimit'  : invest_limit,
            'overview'     : overview,
            'investStatus' : invest_status
        }

        return JsonResponse({"results": results}, status=200)
