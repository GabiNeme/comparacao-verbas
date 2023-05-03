import sys

from src.comparator import Comparator
from src.payment_groups import PaymentGroups
from src.payroll import AerosPayroll, ArtePayroll


def main():
    if len(sys.argv) < 4:
        print(
            'Execute o comando com `python main.py <diretorio_csv_arte>'
            + ' <diretorio_csv_aeros> <diretorio_salvar>`.'
        )
        return

    arte_payroll = ArtePayroll()
    arte_payroll.load_from_file(sys.argv[1])
    aeros_payroll = AerosPayroll()
    aeros_payroll.load_from_file(sys.argv[2])
    payment_group = PaymentGroups()
    payment_group.load_from_file('groups.csv')
    comparator = Comparator(arte_payroll, aeros_payroll, payment_group).compare()

    comparator.to_csv(sys.argv[3], index=False, sep=';')


if __name__ == '__main__':
    main()
