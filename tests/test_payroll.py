import pandas as pd

from src.payroll import AerosPayroll, ArtePayroll


class TestAerosPayroll:
    def test_load_from_file(self):
        file = 'tests/fixture/aeros.csv'

        expected_data = {
            'cm': [1, 1, 2, 2],
            'verba': [1000, 1111, 1000, 1112],
            'valor': [0, 0, 0.01, 197.28],
        }
        expected_df = pd.DataFrame(data=expected_data)

        aeros_payroll = AerosPayroll()
        aeros_payroll.load_from_file(file)
        assert expected_df.equals(aeros_payroll.get())


class TestArtePayroll:
    def test_load_from_file(self):
        file = 'tests/fixture/arte.csv'

        expected_data = {
            'cm': [1, 1, 2, 2],
            'verba': [1000, 1112, 1000, 1111],
            'valor': [0, 0, 0.02, 197.28],
        }
        expected_df = pd.DataFrame(data=expected_data)

        aeros_payroll = ArtePayroll()
        aeros_payroll.load_from_file(file)
        assert expected_df.equals(aeros_payroll.get())
