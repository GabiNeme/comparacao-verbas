import pandas as pd

from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll, Columns, Payroll


class PayrollStub(Payroll):
    def __init__(self):
        payroll = {
            Columns.CM.value: [1, 1, 1, 1, 2, 2],
            Columns.FUND.value: ['3000', '1000', '1010', '2000', '2000', '2020'],
            Columns.VALUE.value: [1000, 1000, 1000, 1000, 0, 0],
        }

        self.df = pd.DataFrame(data=payroll)


class PaymentGroupsStub(PaymentGroups):
    def __init__(self) -> None:
        groups = {
            '1000': 'G1',
            '1010': 'G1',
            '2000': 'G2',
            '2020': 'G2',
        }

        self.groups = groups


class TestPayroll:
    def test_apply(payment_groups: PaymentGroups):

        payroll = PayrollStub()
        payment_groups = PaymentGroupsStub()

        payroll.apply(payment_groups=payment_groups)

        expected_data = {
            Columns.CM.value: [1, 1, 1, 1, 2, 2],
            Columns.FUND.value: ['3000', '1000', '1010', '2000', '2000', '2020'],
            Columns.VALUE.value: [1000, 1000, 1000, 1000, 0, 0],
            Columns.GROUP.value: [None, 'G1', 'G1', 'G2', 'G2', 'G2'],
        }
        expected_df = pd.DataFrame(data=expected_data)

        assert expected_df.equals(payroll.get())


class TestAerosPayroll:
    def test_load_from_file(self):
        file = 'tests/fixture/aeros.csv'

        expected_data = {
            Columns.CM.value: [1, 1, 2, 2],
            Columns.FUND.value: ['1000', '0111', '1000', '1112'],
            Columns.VALUE.value: [0, 0, 0.01, 197.28],
        }
        expected_df = pd.DataFrame(data=expected_data)

        aeros_payroll = AerosPayroll()
        aeros_payroll.load_from_file(file)

        assert expected_df.equals(aeros_payroll.get())


class TestArtePayroll:
    def test_load_from_file(self):
        file = 'tests/fixture/arte.csv'

        expected_data = {
            Columns.CM.value: [1, 1, 2, 2],
            Columns.FUND.value: ['1000', '0112', '1000', '1111'],
            Columns.VALUE.value: [0, 0, 0.02, 197.28],
        }
        expected_df = pd.DataFrame(data=expected_data)

        aeros_payroll = ArtePayroll()
        aeros_payroll.load_from_file(file)

        assert expected_df.equals(aeros_payroll.get())
