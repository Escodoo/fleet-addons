# Copyright 2026 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestFleetVehicleRenavam(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vehicle_model = cls.env["fleet.vehicle"]
        cls.brand_model = cls.env["fleet.vehicle.model.brand"]
        cls.model_model = cls.env["fleet.vehicle.model"]
        cls.test_brand = cls.brand_model.create({"name": "Test Brand"})
        cls.test_model = cls.model_model.create(
            {"name": "Test Model", "brand_id": cls.test_brand.id}
        )

    def _create_vehicle(self, values):
        vals = {
            "name": "Vehicle",
            "model_id": self.test_model.id,
        }
        vals.update(values)
        return self.vehicle_model.create(vals)

    def test_renavam_days_to_expire_with_future_date(self):
        future_date = date.today() + timedelta(days=45)
        vehicle = self._create_vehicle(
            {"name": "Vehicle Future", "renavam_expiry_date": future_date}
        )
        self.assertEqual(vehicle.renavam_days_to_expire, 45)

    def test_renavam_days_to_expire_with_past_date(self):
        past_date = date.today() - timedelta(days=10)
        vehicle = self._create_vehicle(
            {"name": "Vehicle Past", "renavam_expiry_date": past_date}
        )
        self.assertEqual(vehicle.renavam_days_to_expire, -10)

    def test_renavam_days_to_expire_no_date(self):
        vehicle = self._create_vehicle({"name": "Vehicle No Date"})
        self.assertEqual(vehicle.renavam_days_to_expire, 0)

    def test_renavam_expiry_state_no_renavam(self):
        vehicle = self._create_vehicle({"name": "Vehicle No Renavam"})
        self.assertEqual(vehicle.renavam_expiry_state, "no_renavam")

    def test_renavam_expiry_state_expired(self):
        past_date = date.today() - timedelta(days=5)
        vehicle = self._create_vehicle(
            {"name": "Vehicle Expired", "renavam_expiry_date": past_date}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "expired")

    def test_renavam_expiry_state_edge_30_days(self):
        edge_date = date.today() + timedelta(days=30)
        vehicle = self._create_vehicle(
            {"name": "Vehicle 30 Days", "renavam_expiry_date": edge_date}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "expiring_soon")
        self.assertEqual(vehicle.renavam_days_to_expire, 30)

    def test_renavam_expiry_state_edge_31_days(self):
        edge_date = date.today() + timedelta(days=31)
        vehicle = self._create_vehicle(
            {"name": "Vehicle 31 Days", "renavam_expiry_date": edge_date}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "valid")
        self.assertEqual(vehicle.renavam_days_to_expire, 31)

    def test_renavam_expiry_state_edge_0_days(self):
        today = date.today()
        vehicle = self._create_vehicle(
            {"name": "Vehicle Today", "renavam_expiry_date": today}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "expiring_soon")
        self.assertEqual(vehicle.renavam_days_to_expire, 0)

    def test_renavam_state_update_on_date_change(self):
        future_date = date.today() + timedelta(days=60)
        vehicle = self._create_vehicle(
            {"name": "Vehicle Update Date", "renavam_expiry_date": future_date}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "valid")

        soon_date = date.today() + timedelta(days=15)
        vehicle.write({"renavam_expiry_date": soon_date})
        self.assertEqual(vehicle.renavam_expiry_state, "expiring_soon")
        self.assertEqual(vehicle.renavam_days_to_expire, 15)

        past_date = date.today() - timedelta(days=1)
        vehicle.write({"renavam_expiry_date": past_date})
        self.assertEqual(vehicle.renavam_expiry_state, "expired")
        self.assertEqual(vehicle.renavam_days_to_expire, -1)

    def test_renavam_state_update_on_date_removal(self):
        future_date = date.today() + timedelta(days=60)
        vehicle = self._create_vehicle(
            {"name": "Vehicle Remove Date", "renavam_expiry_date": future_date}
        )
        self.assertEqual(vehicle.renavam_expiry_state, "valid")

        vehicle.write({"renavam_expiry_date": False})
        self.assertEqual(vehicle.renavam_expiry_state, "no_renavam")
        self.assertEqual(vehicle.renavam_days_to_expire, 0)

    def test_multiple_vehicles_different_states(self):
        today = date.today()
        vehicles = self.vehicle_model.create(
            [
                {"name": "Vehicle No Date", "model_id": self.test_model.id},
                {
                    "name": "Vehicle Batch Expired",
                    "model_id": self.test_model.id,
                    "renavam_expiry_date": today - timedelta(days=10),
                },
                {
                    "name": "Vehicle Batch Expiring Soon",
                    "model_id": self.test_model.id,
                    "renavam_expiry_date": today + timedelta(days=20),
                },
                {
                    "name": "Vehicle Batch Valid",
                    "model_id": self.test_model.id,
                    "renavam_expiry_date": today + timedelta(days=90),
                },
            ]
        )

        self.assertEqual(vehicles[0].renavam_expiry_state, "no_renavam")
        self.assertEqual(vehicles[1].renavam_expiry_state, "expired")
        self.assertEqual(vehicles[2].renavam_expiry_state, "expiring_soon")
        self.assertEqual(vehicles[3].renavam_expiry_state, "valid")

        self.assertEqual(vehicles[0].renavam_days_to_expire, 0)
        self.assertEqual(vehicles[1].renavam_days_to_expire, -10)
        self.assertEqual(vehicles[2].renavam_days_to_expire, 20)
        self.assertEqual(vehicles[3].renavam_days_to_expire, 90)
