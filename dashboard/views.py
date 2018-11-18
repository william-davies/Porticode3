from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View


# class AuthenticationView(View):
#     def get(self, request, *args, **kwargs):
#         client_id = 'oauth2client_00009cr46xyuBDKxayG0Mj'
#         redirect_uri = 'http://127.0.0.1:8000' + reverse('dashboard:dashboard')
#         response_type = 'code'
#         state = 'abc123'
#         url = 'https://auth.monzo.com/?client_id={}&redirect_uri={}&response_type={}&state={}'.format(client_id, redirect_uri, response_type, state)
#         return redirect(url)
#
# class ReceiveAuthorizationCodeView(View):
#     def get(self, request, *args, **kwargs):
#         return 2
from dashboard.models import transactions_json
from dashboard.utils import get_dates


class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    def get_transaction_tuple(self, transaction):
        if transaction['merchant'] and 'name' in transaction['merchant']:
            transaction_partner = transaction['merchant']['name']
        else:
            transaction_partner = transaction['counterparty']['name']
        # convert amount from pence to pounds
        amount = self.format_amount(transaction['amount'])
        return transaction_partner, amount

    @staticmethod
    def format_amount(amount):
        # convert amount from p to pounds
        amount /= 100
        amount = '{:.2f}'.format(amount)
        if amount[0] == '-':
            # remove minus sign
            amount = '£' + amount[1:]
        else:
            amount = '+£' + amount
        return amount

    def get_datetimes_data(self, datetimes, transactions):
        datetimes_data = []
        for datetime in datetimes:
            transactions_data = []
            for transaction in transactions:
                transaction_datetime = datetime.strptime(transaction['created'][:10], '%Y-%m-%d')
                if transaction_datetime == datetime:
                    transactions_data.append(self.get_transaction_tuple(transaction))
            datetimes_data.append((datetime, transactions_data))
        return datetimes_data


    def get(self, request, *args, **kwargs):
        transactions = transactions_json[-20:]
        dates = get_dates(transactions)
        dates_data = self.get_datetimes_data(dates, transactions)
        return render(request, template_name=self.template_name, context={'dates_data': dates_data})

