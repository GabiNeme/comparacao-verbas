import pandas as pd

from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll, Columns


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
        df[Columns.EQUAL.value] = df[Columns.EQUAL.value].astype('bool')
        df = df.sort_values(
            by=[Columns.CM.value, Columns.GROUP.value, Columns.FUND.value]
        )
        df = df[
            [
                Columns.CM.value,
                Columns.GROUP.value,
                Columns.FUND.value,
                Columns.ARTE_VALUE.value,
                Columns.AEROS_VALUE.value,
                Columns.EQUAL.value,
            ]
        ]
        df = df.reset_index(drop=True)

        return df

    def _merge(self) -> None:

        if self.merged is None:
            self.merged = pd.merge(
                self._arte_payroll.get(),
                self._aeros_payroll.get(),
                how='outer',
                suffixes=('_arte', '_aeros'),
                on=[Columns.CM.value, Columns.FUND.value, Columns.GROUP.value],
            )
            self.merged[Columns.ARTE_VALUE.value] = self.merged[
                Columns.ARTE_VALUE.value
            ].fillna(0)
            self.merged[Columns.AEROS_VALUE.value] = self.merged[
                Columns.AEROS_VALUE.value
            ].fillna(0)

    def _compute_rows_without_group(self):

        df = self.merged[self.merged[Columns.GROUP.value].isnull()].copy()
        df.loc[:, Columns.EQUAL.value] = (
            df[Columns.ARTE_VALUE.value] == df[Columns.AEROS_VALUE.value]
        )

        return df

    def _compute_rows_with_group(self):

        df = self.merged[self.merged[Columns.GROUP.value].notnull()].copy()

        df_sum = df.groupby([Columns.CM.value, Columns.GROUP.value]).sum(
            numeric_only=True
        )
        df_sum[Columns.EQUAL.value] = (
            abs(df_sum[Columns.ARTE_VALUE.value] - df_sum[Columns.AEROS_VALUE.value]) < 0.001
        )

        for index, row in df_sum.iterrows():
            criteria = (df[Columns.CM.value] == index[0]) & (
                df[Columns.GROUP.value] == index[1]
            )
            df.loc[criteria, Columns.EQUAL.value] = row[Columns.EQUAL.value]

        return df
