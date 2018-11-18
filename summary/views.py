from datetime import datetime
import calendar

from django.shortcuts import render

# Create your views here.
from django.views import View

from dashboard.models import balance_json, transactions_json


class SummaryView(View):
    template_name = 'summary/summary.html'

    def get_dates(self):
        today = datetime.today()
        year = today.year
        month = today.month
        tuple = calendar.monthrange(year, month)
        number_days = tuple[1]

        datetimes = []
        for day in range(1, number_days + 1):
            date = datetime(year=year, month=month, day=day)
            datetimes.append(date)
        return month, datetimes

    def get_balances(self, datetimes, month_transactions):
        balance = balance_json['balance']
        balances = [balance]
        previous_balance = balance
        today = datetime.today()
        day = today.day

        for date in datetimes[:day+1]:
            for transaction in month_transactions:
                transaction_datetime = date.strptime(transaction['created'][:10], '%Y-%m-%d')
                if transaction_datetime == date:
                    # the 'amount' of a payment is negative. we're going backwards in time.
                    previous_balance -= transaction['amount']
                elif transaction_datetime < date:
                    break
            balances.append(previous_balance)
        for date in datetimes[day+1:]:
            balances.insert(0, balance)
        chronological_balance = balances[::-1]
        return chronological_balance


    def get_month_transactions(self, month, transactions):
        month_transactions = []
        for transaction in transactions:
            transaction_datetime = datetime.strptime(transaction['created'][:10], '%Y-%m-%d')
            if transaction_datetime.month == month:
                month_transactions.append(transaction)
        chron_month_transactions = month_transactions[::-1]
        return month_transactions


    def get(self, request, *args, **kwargs):
        month, datetimes = self.get_dates()
        transactions = transactions_json[-200:]
        transactions.reverse()
        month_transactions = self.get_month_transactions(month, transactions)
        balances = self.get_balances(datetimes, month_transactions)
        return render(request, template_name=self.template_name)