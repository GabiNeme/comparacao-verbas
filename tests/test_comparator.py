import numpy as np
import pandas as pd

from src.comparator import Comparator
from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll


class ArtePayrollStub(ArtePayroll):
    def __init__(self):
        arte_payroll = {
            "cm": [1, 1, 1, 1, 1, 2, 2, 2, 2],
            "verba": [
                "3000",
                "1000",
                "1010",
                "2000",
                "2020",
                "1000",
                "3000",
                "2000",
                "2020",
            ],
            "valor": [1000, 1000, 1000, 500, 1000, 1000, 1000, 1000, 0],
        }

        self.df = pd.DataFrame(data=arte_payroll)


class AerosPayrollStub(AerosPayroll):
    def __init__(self):
        aeros_payroll = {
            "cm": [1, 1, 1, 1, 1, 1, 3, 2, 2],
            "verba": [
                "3000",
                "1000",
                "1010",
                "2000",
                "2020",
                "4000",
                "1000",
                "2000",
                "2020",
            ],
            "valor": [1000, 1000, 1000, 1000, 500, 1000, 1000, 0, 0],
        }

        self.df = pd.DataFrame(data=aeros_payroll)


class PaymentGroupsStub(PaymentGroups):
    def __init__(self):
        groups = {
            "1000": "G1",
            "1010": "G1",
            "2000": "G2",
            "2020": "G2",
        }

        self.groups = groups


class TestComparator:
    def test_compare(self):

        expected_result = {
            "cm": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3],
            "grupo": [
                np.nan,
                "G1",
                "G1",
                "G2",
                "G2",
                np.nan,
                "G1",
                np.nan,
                "G2",
                "G2",
                "G1",
            ],
            "verba": [
                "3000",
                "1000",
                "1010",
                "2000",
                "2020",
                "4000",
                "1000",
                "3000",
                "2000",
                "2020",
                "1000",
            ],
            "valor_arte": [1000.0, 1000, 1000, 500, 1000, 0, 1000, 1000, 1000, 0, 0],
            "valor_aeros": [1000.0, 1000, 1000, 1000, 500, 1000, 0, 0, 0, 0, 1000],
            "igual": [
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
        expected_df = expected_df.sort_values(by=["cm", "grupo", "verba"])
        expected_df = expected_df.reset_index(drop=True)

        arte_payroll = ArtePayrollStub()
        aeros_payroll = AerosPayrollStub()
        payment_group = PaymentGroupsStub()
        comparator = Comparator(arte_payroll, aeros_payroll, payment_group)

        result = comparator.compare()

        assert expected_df.equals(result)
