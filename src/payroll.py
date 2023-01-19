from enum import Enum

import pandas as pd

from src.payment_groups import PaymentGroups


class Columns(Enum):
    CM = 'cm'
    FUND = 'verba'
    GROUP = 'grupo'
    VALUE = 'valor'
    ARTE_VALUE = 'valor_arte'
    AEROS_VALUE = 'valor_aeros'
    EQUAL = 'igual'


class Payroll:
    def __init__(self) -> None:
        self.df = None

    def load_from_file(self, file):
        pass

    def get(self):
        return self.df

    def apply(self, payment_groups: PaymentGroups):
        self.df[Columns.GROUP.value] = self.df[Columns.FUND.value].map(
            payment_groups.get()
        )


class AerosPayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file, sep=';', dtype={Columns.FUND.value: 'object'})

        # remove last empty column
        self.df = self.df.drop(self.df.columns[3], axis=1)


class ArtePayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file, dtype={Columns.FUND.value: 'object'})
