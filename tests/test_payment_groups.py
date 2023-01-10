from src.payment_groups import PaymentGroups


class TestPaymentGroups:

    def test_load_from_file(self):
        file = 'tests/fixture/groups.csv'

        expected_groups = {
            'GRUPO1': ['1000', '1010'],
            'GRUPO2': ['2U33', '2U01'],
            'GRUPO3': ['1111', '1112'],
        }
        payment_groups = PaymentGroups()
        payment_groups.load_from_file(file)

        assert expected_groups == payment_groups.get()
