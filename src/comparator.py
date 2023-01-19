import pandas as pd

from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll


class Comparator:
    def __init__(
        self,
        arte_payroll: ArtePayroll,
        aeros_payroll: AerosPayroll,
        payment_groups: PaymentGroups,
    ) -> None:
        self._arte_payroll = arte_payroll
        self._aeros_payroll = aeros_payroll
        self._payment_groups = payment_groups
        self.merged = None

    def compare(self):

        self._aeros_payroll.apply(self._payment_groups)
        self._arte_payroll.apply(self._payment_groups)

        self._merge()

        df_dont_have_group = self._compute_rows_without_group()
        df_have_group = self._compute_rows_with_group()

        df = pd.concat([df_dont_have_group, df_have_group], ignore_index=True)
        df["igual"] = df["igual"].astype("bool")
        df = df.sort_values(by=["cm", "grupo", "verba"])
        df = df[["cm", "grupo", "verba", "valor_arte", "valor_aeros", "igual"]]
        df = df.reset_index(drop=True)

        return df

    def _merge(self) -> None:

        if self.merged is None:
            self.merged = pd.merge(
                self._arte_payroll.get(),
                self._aeros_payroll.get(),
                how="outer",
                suffixes=("_arte", "_aeros"),
                on=["cm", "verba", "grupo"],
            )
            self.merged["valor_arte"] = self.merged["valor_arte"].fillna(0)
            self.merged["valor_aeros"] = self.merged["valor_aeros"].fillna(0)

    def _compute_rows_without_group(self):

        df = self.merged[self.merged["grupo"].isnull()].copy()
        df.loc[:, "igual"] = df["valor_arte"] == df["valor_aeros"]

        return df

    def _compute_rows_with_group(self):

        df = self.merged[self.merged["grupo"].notnull()].copy()

        df_sum = df.groupby(["cm", "grupo"]).sum(numeric_only=True)
        df_sum["igual"] = df_sum["valor_arte"] == df_sum["valor_aeros"]

        for index, row in df_sum.iterrows():
            criteria = (df["cm"] == index[0]) & (df["grupo"] == index[1])
            df.loc[criteria, "igual"] = row["igual"]

        return df
