import pandas as pd


class Payroll:
    def __init__(self) -> None:
        self.df = None

    def load_from_file(self, file):
        pass

    def get(self):
        return self.df


class AerosPayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file, sep=';')

        # remove last empty column
        self.df = self.df.drop(self.df.columns[3], axis=1)


class ArtePayroll(Payroll):
    def load_from_file(self, file):
        self.df = pd.read_csv(file)
