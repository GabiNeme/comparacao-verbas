from src.comparator import Comparator
from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll


def main():

    arte_payroll = ArtePayroll()
    arte_payroll.load_from_file('arte.csv')
    aeros_payroll = AerosPayroll()
    aeros_payroll.load_from_file('aeros.csv')
    payment_group = PaymentGroups()
    payment_group.load_from_file('groups.csv')
    comparator = Comparator(arte_payroll, aeros_payroll, payment_group).compare()

    comparator.to_csv('resultado.csv', index=False, sep=';')


main()
