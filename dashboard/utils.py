from datetime import datetime


def get_dates(transactions):
    datetimes = []
    for transaction in transactions:
        transaction_date = transaction['created'][:10]
        transaction_datetime = datetime.strptime(transaction_date, '%Y-%m-%d')
        if transaction_datetime not in datetimes:
            datetimes.append(transaction_datetime)
    return datetimes