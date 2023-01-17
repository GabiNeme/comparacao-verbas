from src.payment_groups import PaymentGroups


class TestPaymentGroups:

    def test_load_from_file(self):
        file = 'tests/fixture/groups.csv'

        expected_groups = {
            '1000': 'GRUPO1',
            '1010': 'GRUPO1',
            '2U33': 'GRUPO2',
            '2U01': 'GRUPO2',
            '1111': 'GRUPO3',
            '1112': 'GRUPO3',
        }
        payment_groups = PaymentGroups()
        payment_groups.load_from_file(file)

        assert expected_groups == payment_groups.get()
