import unittest
import pandas as pd
from analyse import build_analysis

class DeliveryTests(unittest.TestCase):
    def inputs(self):
        orders = pd.DataFrame({
            'order_id': ['a', 'b', 'c'],
            'customer_id': ['x', 'x', 'x'],
            'order_status': ['delivered', 'delivered', 'canceled'],
            'order_purchase_timestamp': ['2020-01-01'] * 3,
            'order_delivered_customer_date':
                ['2020-01-03 15:00:00', '2020-01-04 01:00:00', None],
            'order_estimated_delivery_date': ['2020-01-03'] * 3
        })
        customers = pd.DataFrame({
            'customer_id': ['x'], 'customer_state': ['SP']
        })
        return orders, customers
    def test_calendar_deadline_and_exclusions(self):
        orders, customers = self.inputs()
        clean, rejected = build_analysis(orders, customers)
        self.assertEqual(clean['is_late'].tolist(), [False, True])
        self.assertEqual(len(rejected), 1)
    def test_duplicate_customer_is_rejected(self):
        orders, customers = self.inputs()
        with self.assertRaises(ValueError):
            build_analysis(orders, pd.concat([customers, customers]))

if __name__ == '__main__':
    unittest.main()
