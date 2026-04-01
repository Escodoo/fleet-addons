# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestHrEmployeeCNH(TransactionCase):
    """Test CNH expiration tracking for HR employees."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee_model = cls.env["hr.employee"]

    def test_cnh_days_to_expire_with_future_date(self):
        """Test cnh_days_to_expire calculation with future expiration date."""
        future_date = date.today() + timedelta(days=45)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Future",
                "driver_license": "12345678901",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            45,
            "Days to expire should be 45 for expiration date 45 days in future",
        )

    def test_cnh_days_to_expire_with_past_date(self):
        """Test cnh_days_to_expire calculation with past expiration date."""
        past_date = date.today() - timedelta(days=10)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Past",
                "driver_license": "12345678902",
                "expiration_date": past_date,
            }
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            -10,
            "Days to expire should be -10 for expiration date 10 days in past",
        )

    def test_cnh_days_to_expire_no_expiration_date(self):
        """Test cnh_days_to_expire when no expiration date is set."""
        employee = self.employee_model.create(
            {
                "name": "Test Employee No Date",
                "driver_license": "12345678903",
            }
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            0,
            "Days to expire should be 0 when no expiration date is set",
        )

    def test_cnh_expiry_state_no_cnh(self):
        """Test cnh_expiry_state when employee has no driver license."""
        employee = self.employee_model.create(
            {
                "name": "Test Employee No CNH",
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "no_cnh",
            "State should be 'no_cnh' when driver_license is not set",
        )

    def test_cnh_expiry_state_no_cnh_with_date(self):
        """Test cnh_expiry_state when no driver license but date is set."""
        future_date = date.today() + timedelta(days=60)
        employee = self.employee_model.create(
            {
                "name": "Test Employee No CNH With Date",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "no_cnh",
            "State should be 'no_cnh' even with expiration date if no driver_license",
        )

    def test_cnh_expiry_state_expired(self):
        """Test cnh_expiry_state when CNH is expired."""
        past_date = date.today() - timedelta(days=5)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Expired",
                "driver_license": "12345678904",
                "expiration_date": past_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "expired",
            "State should be 'expired' when expiration date is in the past",
        )

    def test_cnh_expiry_state_expiring_soon(self):
        """Test cnh_expiry_state when CNH is expiring soon."""
        soon_date = date.today() + timedelta(days=15)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Expiring Soon",
                "driver_license": "12345678905",
                "expiration_date": soon_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "expiring_soon",
            "State should be 'expiring_soon' when expiration date is within 30 days",
        )

    def test_cnh_expiry_state_valid(self):
        """Test cnh_expiry_state when CNH is valid."""
        future_date = date.today() + timedelta(days=60)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Valid",
                "driver_license": "12345678906",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "valid",
            "State should be 'valid' when expiration date is more than 30 days away",
        )

    def test_cnh_expiry_state_edge_30_days(self):
        """Test cnh_expiry_state edge case: exactly 30 days until expiration."""
        edge_date = date.today() + timedelta(days=30)
        employee = self.employee_model.create(
            {
                "name": "Test Employee 30 Days",
                "driver_license": "12345678907",
                "expiration_date": edge_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "expiring_soon",
            "State should be 'expiring_soon' when exactly 30 days until expiration",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            30,
            "Days to expire should be exactly 30",
        )

    def test_cnh_expiry_state_edge_31_days(self):
        """Test cnh_expiry_state edge case: exactly 31 days until expiration."""
        edge_date = date.today() + timedelta(days=31)
        employee = self.employee_model.create(
            {
                "name": "Test Employee 31 Days",
                "driver_license": "12345678908",
                "expiration_date": edge_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "valid",
            "State should be 'valid' when exactly 31 days until expiration",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            31,
            "Days to expire should be exactly 31",
        )

    def test_cnh_expiry_state_edge_0_days(self):
        """Test cnh_expiry_state edge case: expires today."""
        today = date.today()
        employee = self.employee_model.create(
            {
                "name": "Test Employee Today",
                "driver_license": "12345678909",
                "expiration_date": today,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "expiring_soon",
            "State should be 'expiring_soon' when expiration date is today (0 days)",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            0,
            "Days to expire should be exactly 0",
        )

    def test_cnh_expiry_state_edge_negative_1_day(self):
        """Test cnh_expiry_state edge case: expired yesterday."""
        yesterday = date.today() - timedelta(days=1)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Yesterday",
                "driver_license": "12345678910",
                "expiration_date": yesterday,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "expired",
            "State should be 'expired' when expiration date was yesterday (-1 days)",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            -1,
            "Days to expire should be exactly -1",
        )

    def test_cnh_state_update_on_date_change(self):
        """Test that cnh_expiry_state updates when expiration_date changes."""
        # Create employee with valid CNH
        future_date = date.today() + timedelta(days=60)
        employee = self.employee_model.create(
            {
                "name": "Test Employee Update",
                "driver_license": "12345678911",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "valid",
            "Initial state should be 'valid'",
        )

        # Update to expiring soon
        soon_date = date.today() + timedelta(days=15)
        employee.write({"expiration_date": soon_date})
        self.assertEqual(
            employee.cnh_expiry_state,
            "expiring_soon",
            "State should update to 'expiring_soon' after date change",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            15,
            "Days to expire should update to 15",
        )

        # Update to expired
        past_date = date.today() - timedelta(days=5)
        employee.write({"expiration_date": past_date})
        self.assertEqual(
            employee.cnh_expiry_state,
            "expired",
            "State should update to 'expired' after date change",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            -5,
            "Days to expire should update to -5",
        )

    def test_cnh_state_update_on_license_removal(self):
        """Test that cnh_expiry_state updates when driver license is removed."""
        future_date = date.today() + timedelta(days=60)
        employee = self.employee_model.create(
            {
                "name": "Test Employee License Removal",
                "driver_license": "12345678912",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "valid",
            "Initial state should be 'valid'",
        )

        # Remove driver license
        employee.write({"driver_license": False})
        self.assertEqual(
            employee.cnh_expiry_state,
            "no_cnh",
            "State should update to 'no_cnh' when driver_license is removed",
        )

    def test_cnh_state_update_on_license_addition(self):
        """Test that cnh_expiry_state updates when driver license is added."""
        future_date = date.today() + timedelta(days=60)
        employee = self.employee_model.create(
            {
                "name": "Test Employee License Addition",
                "expiration_date": future_date,
            }
        )
        self.assertEqual(
            employee.cnh_expiry_state,
            "no_cnh",
            "Initial state should be 'no_cnh'",
        )

        # Add driver license
        employee.write({"driver_license": "12345678913"})
        self.assertEqual(
            employee.cnh_expiry_state,
            "valid",
            "State should update to 'valid' when driver_license is added",
        )
        self.assertEqual(
            employee.cnh_days_to_expire,
            60,
            "Days to expire should be calculated after license addition",
        )

    def test_multiple_employees_different_states(self):
        """Test multiple employees with different CNH states."""
        today = date.today()
        employees = self.employee_model.create(
            [
                {
                    "name": "Employee No CNH",
                },
                {
                    "name": "Employee Expired",
                    "driver_license": "11111111111",
                    "expiration_date": today - timedelta(days=10),
                },
                {
                    "name": "Employee Expiring Soon",
                    "driver_license": "22222222222",
                    "expiration_date": today + timedelta(days=20),
                },
                {
                    "name": "Employee Valid",
                    "driver_license": "33333333333",
                    "expiration_date": today + timedelta(days=90),
                },
            ]
        )

        self.assertEqual(employees[0].cnh_expiry_state, "no_cnh")
        self.assertEqual(employees[1].cnh_expiry_state, "expired")
        self.assertEqual(employees[2].cnh_expiry_state, "expiring_soon")
        self.assertEqual(employees[3].cnh_expiry_state, "valid")

        self.assertEqual(employees[0].cnh_days_to_expire, 0)
        self.assertEqual(employees[1].cnh_days_to_expire, -10)
        self.assertEqual(employees[2].cnh_days_to_expire, 20)
        self.assertEqual(employees[3].cnh_days_to_expire, 90)
