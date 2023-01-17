import pandas as pd

from src.payment_groups import PaymentGroups


class Payroll:
    def __init__(self) -> None:
        self.df = None

    def load_from_file(self, file):
        pass

    def get(self):
        return self.df

    def apply(self, payment_groups: PaymentGroups):
        self.df['grupo'] = self.df['verba'].map(payment_groups.get())


class AerosPayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file, sep=';', dtype={'verba': 'object'})

        # remove last empty column
        self.df = self.df.drop(self.df.columns[3], axis=1)


class ArtePayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file, dtype={'verba': 'object'})
