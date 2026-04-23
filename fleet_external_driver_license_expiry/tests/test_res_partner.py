# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestResPartnerLicense(TransactionCase):
    """Test Driver License expiration tracking for external drivers."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_driver_license_expiry(self):
        """Test multiple partners with different Driver License states."""
        today = date.today()
        drivers = self.partner_model.create(
            [
                {
                    "name": "Driver No Licencse",
                },
                {
                    "name": "Driver Expired",
                    "driver_license_number": "11111111111",
                    "driver_license_expiration_date": today - timedelta(days=10),
                },
                {
                    "name": "Driver Expiring Soon",
                    "driver_license_number": "22222222222",
                    "driver_license_expiration_date": today + timedelta(days=20),
                },
                {
                    "name": "Driver Valid",
                    "driver_license_number": "33333333333",
                    "driver_license_expiration_date": today + timedelta(days=90),
                },
            ]
        )

        self.assertEqual(drivers[0].driver_license_days_to_expire, 0)
        self.assertEqual(drivers[1].driver_license_days_to_expire, -10)
        self.assertEqual(drivers[2].driver_license_days_to_expire, 20)
        self.assertEqual(drivers[3].driver_license_days_to_expire, 90)

        self.assertEqual(drivers[0].driver_license_expiry_state, "no_license")
        self.assertEqual(drivers[1].driver_license_expiry_state, "expired")
        self.assertEqual(drivers[2].driver_license_expiry_state, "expiring_soon")
        self.assertEqual(drivers[3].driver_license_expiry_state, "valid")
