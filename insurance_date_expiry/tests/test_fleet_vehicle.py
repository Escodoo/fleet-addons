# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestFleetVehicleInsurance(TransactionCase):
    """Test fleet vehicle insurance expiry functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level data for all test methods."""
        super().setUpClass()
        cls.vehicle_model = cls.env["fleet.vehicle"]

        cls.today = fields.Date.today()
        cls.yesterday = cls.today - timedelta(days=1)
        cls.tomorrow = cls.today + timedelta(days=1)
        cls.next_week = cls.today + timedelta(days=7)
        cls.next_month = cls.today + timedelta(days=35)

        cls.vehicle_no_insurance = cls.vehicle_model.create(
            {
                "license_plate": "NO-INS-001",
                "vin_sn": "1HGCM82633A000000",
                "model_id": cls.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": False,
            }
        )

        cls.vehicle_expired = cls.vehicle_model.create(
            {
                "license_plate": "EXP-001",
                "vin_sn": "1HGCM82633A000001",
                "model_id": cls.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": cls.yesterday,
            }
        )

        cls.vehicle_expiring_soon = cls.vehicle_model.create(
            {
                "license_plate": "EXP-SOON-001",
                "vin_sn": "1HGCM82633A000002",
                "model_id": cls.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": cls.tomorrow,
            }
        )

        cls.vehicle_expiring_week = cls.vehicle_model.create(
            {
                "license_plate": "EXP-WEEK-001",
                "vin_sn": "1HGCM82633A000003",
                "model_id": cls.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": cls.next_week,
            }
        )

        cls.vehicle_valid = cls.vehicle_model.create(
            {
                "license_plate": "VALID-001",
                "vin_sn": "1HGCM82633A000004",
                "model_id": cls.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": cls.next_month,
            }
        )

    def test_insurance_days_to_expire_no_insurance(self):
        """Test days to expire when no insurance date is set."""
        self.assertEqual(
            self.vehicle_no_insurance.insurance_days_to_expire,
            0,
            "Days to expire should be 0 when no insurance date is set",
        )

    def test_insurance_days_to_expire_expired(self):
        """Test days to expire for expired insurance."""
        expected_days = (self.yesterday - self.today).days
        self.assertEqual(
            self.vehicle_expired.insurance_days_to_expire,
            expected_days,
            "Days to expire should be negative for expired insurance",
        )
        self.assertLess(
            self.vehicle_expired.insurance_days_to_expire,
            0,
            "Days to expire should be less than 0 for expired insurance",
        )

    def test_insurance_days_to_expire_expiring_soon(self):
        """Test days to expire for insurance expiring soon."""
        expected_days = (self.tomorrow - self.today).days
        self.assertEqual(
            self.vehicle_expiring_soon.insurance_days_to_expire,
            expected_days,
            "Days to expire should match calculated days for expiring soon insurance",
        )
        self.assertGreaterEqual(
            self.vehicle_expiring_soon.insurance_days_to_expire,
            0,
            "Days to expire should be non-negative for future insurance",
        )
        self.assertLessEqual(
            self.vehicle_expiring_soon.insurance_days_to_expire,
            30,
            "Days to expire should be <= 30 for expiring soon insurance",
        )

    def test_insurance_days_to_expire_valid(self):
        """Test days to expire for valid insurance."""
        expected_days = (self.next_month - self.today).days
        self.assertEqual(
            self.vehicle_valid.insurance_days_to_expire,
            expected_days,
            "Days to expire should match calculated days for valid insurance",
        )
        self.assertGreater(
            self.vehicle_valid.insurance_days_to_expire,
            30,
            "Days to expire should be > 30 for valid insurance",
        )

    def test_insurance_expiry_state_no_insurance(self):
        """Test expiry state when no insurance date is set."""
        self.assertEqual(
            self.vehicle_no_insurance.insurance_expiry_state,
            "no_insurance",
            "Expiry state should be 'no_insurance' when no insurance date is set",
        )

    def test_insurance_expiry_state_expired(self):
        """Test expiry state for expired insurance."""
        self.assertEqual(
            self.vehicle_expired.insurance_expiry_state,
            "expired",
            "Expiry state should be 'expired' for past insurance date",
        )

    def test_insurance_expiry_state_expiring_soon(self):
        """Test expiry state for insurance expiring soon."""
        self.assertEqual(
            self.vehicle_expiring_soon.insurance_expiry_state,
            "expiring_soon",
            "Expiry state should be 'expiring_soon' for insurance within 30 days",
        )

        self.assertEqual(
            self.vehicle_expiring_week.insurance_expiry_state,
            "expiring_soon",
            "Expiry state should be 'expiring_soon' for insurance within 30 days",
        )

    def test_insurance_expiry_state_valid(self):
        """Test expiry state for valid insurance."""
        self.assertEqual(
            self.vehicle_valid.insurance_expiry_state,
            "valid",
            "Expiry state should be 'valid' for insurance more than 30 days away",
        )

    def test_insurance_date_change_updates_computed_fields(self):
        """Test that changing insurance date updates computed fields."""
        vehicle = self.vehicle_no_insurance
        self.assertEqual(vehicle.insurance_expiry_state, "no_insurance")
        self.assertEqual(vehicle.insurance_days_to_expire, 0)

        # Changing the dependency should automatically trigger recompute on next access
        vehicle.insurance_date_expiry = self.tomorrow

        self.assertEqual(vehicle.insurance_expiry_state, "expiring_soon")
        self.assertEqual(vehicle.insurance_days_to_expire, 1)

        vehicle.insurance_date_expiry = self.next_month

        self.assertEqual(vehicle.insurance_expiry_state, "valid")
        self.assertGreater(vehicle.insurance_days_to_expire, 30)

    def test_insurance_selection_values(self):
        """Test that insurance expiry state has correct selection values."""
        selection_values = dict(
            self.vehicle_model._fields["insurance_expiry_state"].selection
        )
        expected_values = {
            "valid": "Valid",
            "expiring_soon": "Expiring Soon",
            "expired": "Expired",
            "no_insurance": "No Insurance",
        }

        for key, value in expected_values.items():
            self.assertIn(key, selection_values)
            self.assertEqual(selection_values[key], value)

    def test_multiple_vehicles_batch_computation(self):
        """Test batch computation of insurance fields for multiple vehicles."""
        test_dates = [
            False,  # No insurance
            self.yesterday - timedelta(days=4),  # Expired
            self.tomorrow,  # Expiring soon
            self.today + timedelta(days=15),  # Expiring soon
            self.today + timedelta(days=45),  # Valid
        ]

        vehicles = self.vehicle_model
        for i, expiry_date in enumerate(test_dates):
            vehicle = self.vehicle_model.create(
                {
                    "license_plate": f"BATCH-{i:03d}",
                    "vin_sn": f"1HGCM82633A000{i:05d}",
                    "model_id": self.env.ref("fleet.model_astra").id,
                    "insurance_date_expiry": expiry_date,
                }
            )
            vehicles |= vehicle

        # Trigger batch computation by accessing the field on the recordset
        # or explicitly calling the compute method if needed for coverage.
        vehicles._compute_insurance_days_to_expire()
        vehicles._compute_insurance_expiry_state()

        expected_states = [
            "no_insurance",
            "expired",
            "expiring_soon",
            "expiring_soon",
            "valid",
        ]

        for vehicle, expected_state in zip(vehicles, expected_states, strict=True):
            self.assertEqual(
                vehicle.insurance_expiry_state,
                expected_state,
                f"Vehicle {vehicle.license_plate} should have state {expected_state}",
            )

    def test_edge_case_exactly_30_days(self):
        """Test insurance state exactly 30 days from today."""
        exactly_30_days = self.today + timedelta(days=30)

        vehicle = self.vehicle_model.create(
            {
                "license_plate": "EDGE-30",
                "vin_sn": "1HGCM82633A000030",
                "model_id": self.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": exactly_30_days,
            }
        )

        self.assertEqual(vehicle.insurance_days_to_expire, 30)
        self.assertEqual(vehicle.insurance_expiry_state, "expiring_soon")

    def test_edge_case_exactly_31_days(self):
        """Test insurance state exactly 31 days from today."""
        exactly_31_days = self.today + timedelta(days=31)

        vehicle = self.vehicle_model.create(
            {
                "license_plate": "EDGE-31",
                "vin_sn": "1HGCM82633A000031",
                "model_id": self.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": exactly_31_days,
            }
        )

        self.assertEqual(vehicle.insurance_days_to_expire, 31)
        self.assertEqual(vehicle.insurance_expiry_state, "valid")

    def test_insurance_fields_readonly(self):
        """Test that computed fields are readonly."""
        vehicle = self.vehicle_model.create(
            {
                "license_plate": "READONLY-001",
                "vin_sn": "1HGCM82633A000099",
                "model_id": self.env.ref("fleet.model_astra").id,
                "insurance_date_expiry": self.today + timedelta(days=10),
            }
        )

        self.assertTrue(vehicle._fields["insurance_days_to_expire"].readonly)
        self.assertTrue(vehicle._fields["insurance_expiry_state"].readonly)
