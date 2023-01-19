import numpy as np
import pandas as pd

from src.comparator import Comparator
from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll, Columns


class ArtePayrollStub(ArtePayroll):
    def __init__(self):
        arte_payroll = {
            Columns.CM.value: [1, 1, 1, 1, 1, 2, 2, 2, 2],
            Columns.FUND.value: [
                '3000',
                '1000',
                '1010',
                '2000',
                '2020',
                '1000',
                '3000',
                '2000',
                '2020',
            ],
            Columns.VALUE.value: [1000, 1000, 1000, 500, 1000, 1000, 1000, 1000, 0],
        }

        self.df = pd.DataFrame(data=arte_payroll)


class AerosPayrollStub(AerosPayroll):
    def __init__(self):
        aeros_payroll = {
            Columns.CM.value: [1, 1, 1, 1, 1, 1, 3, 2, 2],
            Columns.FUND.value: [
                '3000',
                '1000',
                '1010',
                '2000',
                '2020',
                '4000',
                '1000',
                '2000',
                '2020',
            ],
            Columns.VALUE.value: [1000, 1000, 1000, 1000, 500, 1000, 1000, 0, 0],
        }

        self.df = pd.DataFrame(data=aeros_payroll)


class PaymentGroupsStub(PaymentGroups):
    def __init__(self):
        groups = {
            '1000': 'G1',
            '1010': 'G1',
            '2000': 'G2',
            '2020': 'G2',
        }

        self.groups = groups


class TestComparator:
    def test_compare(self):

        expected_result = {
            Columns.CM.value: [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3],
            Columns.GROUP.value: [
                np.nan,
                'G1',
                'G1',
                'G2',
                'G2',
                np.nan,
                'G1',
                np.nan,
                'G2',
                'G2',
                'G1',
            ],
            Columns.FUND.value: [
                '3000',
                '1000',
                '1010',
                '2000',
                '2020',
                '4000',
                '1000',
                '3000',
                '2000',
                '2020',
                '1000',
            ],
            'valor_arte': [1000.0, 1000, 1000, 500, 1000, 0, 1000, 1000, 1000, 0, 0],
            'valor_aeros': [1000.0, 1000, 1000, 1000, 500, 1000, 0, 0, 0, 0, 1000],
            'igual': [
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        }
        expected_df = pd.DataFrame(data=expected_result)
        expected_df = expected_df.sort_values(
            by=[Columns.CM.value, Columns.GROUP.value, Columns.FUND.value]
        )
        expected_df = expected_df.reset_index(drop=True)

        arte_payroll = ArtePayrollStub()
        aeros_payroll = AerosPayrollStub()
        payment_group = PaymentGroupsStub()
        comparator = Comparator(arte_payroll, aeros_payroll, payment_group)

        result = comparator.compare()

        assert expected_df.equals(result)
