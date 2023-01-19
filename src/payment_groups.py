import pandas as pd


class PaymentGroups:
    def __init__(self) -> None:
        self.groups = {}

    def load_from_file(self, file):

        df = pd.read_csv(file, sep=';')

        for _, row in df.iterrows():
            self.groups[row['Verba']] = row['Grupo']

    def get(self):
        return self.groups
