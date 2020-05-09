class BankMarketViewModel(object):
    def __init__(self, id, name, total, rang, avg, ecart_type, data_per_date):
        self.id = id,
        self.name = name,
        self.total = total,
        self.rang = rang,
        self.avg = avg,
        self.ecart_type = ecart_type,
        self.dates = data_per_date


class Data_per_date(object):
    def __init__(self, period, data):
        self.period = period,
        self.data = data

