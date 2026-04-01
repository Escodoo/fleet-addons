# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestFleetVehicle(TransactionCase):
    """Test cases for fleet.vehicle IPVA expiry functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test data using class method."""
        super().setUpClass()

        # Create a vehicle model for testing
        cls.vehicle_model = cls.env["fleet.vehicle.model"].create(
            {
                "name": "Test Model",
                "brand_id": cls.env["fleet.vehicle.model.brand"]
                .create({"name": "Test Brand"})
                .id,
            }
        )

        # Create test vehicles with different IPVA scenarios
        cls.today = date.today()

        # Vehicle with valid IPVA (more than 30 days)
        cls.vehicle_valid = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle Valid IPVA",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": cls.today + timedelta(days=60),
            }
        )

        # Vehicle with IPVA expiring soon (exactly 30 days)
        cls.vehicle_expiring_30 = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle Expiring 30 Days",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": cls.today + timedelta(days=30),
            }
        )

        # Vehicle with IPVA expiring soon (less than 30 days)
        cls.vehicle_expiring_soon = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle Expiring Soon",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": cls.today + timedelta(days=15),
            }
        )

        # Vehicle with IPVA expiring today (0 days)
        cls.vehicle_expiring_today = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle Expiring Today",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": cls.today,
            }
        )

        # Vehicle with expired IPVA (negative days)
        cls.vehicle_expired = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle Expired IPVA",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": cls.today - timedelta(days=10),
            }
        )

        # Vehicle without IPVA date
        cls.vehicle_no_ipva = cls.env["fleet.vehicle"].create(
            {
                "name": "Vehicle No IPVA",
                "model_id": cls.vehicle_model.id,
                "ipva_expiry_date": False,
            }
        )

    def test_compute_ipva_days_to_expire_valid(self):
        """Test computation of days to expire for valid IPVA."""
        self.assertEqual(
            self.vehicle_valid.ipva_days_to_expire,
            60,
            "Days to expire should be 60 for vehicle with IPVA expiring in 60 days",
        )

    def test_compute_ipva_days_to_expire_expiring_soon(self):
        """Test computation of days to expire for IPVA expiring soon."""
        self.assertEqual(
            self.vehicle_expiring_soon.ipva_days_to_expire,
            15,
            "Days to expire should be 15 for vehicle with IPVA expiring in 15 days",
        )

    def test_compute_ipva_days_to_expire_expiring_30(self):
        """Test computation of days to expire for IPVA expiring in exactly 30 days."""
        self.assertEqual(
            self.vehicle_expiring_30.ipva_days_to_expire,
            30,
            "Days to expire should be 30 for vehicle with IPVA expiring in 30 days",
        )

    def test_compute_ipva_days_to_expire_today(self):
        """Test computation of days to expire for IPVA expiring today."""
        self.assertEqual(
            self.vehicle_expiring_today.ipva_days_to_expire,
            0,
            "Days to expire should be 0 for vehicle with IPVA expiring today",
        )

    def test_compute_ipva_days_to_expire_expired(self):
        """Test computation of days to expire for expired IPVA."""
        self.assertEqual(
            self.vehicle_expired.ipva_days_to_expire,
            -10,
            "Days to expire should be -10 for vehicle with IPVA expired 10 days ago",
        )

    def test_compute_ipva_days_to_expire_no_date(self):
        """Test computation of days to expire when no IPVA date is set."""
        self.assertEqual(
            self.vehicle_no_ipva.ipva_days_to_expire,
            0,
            "Days to expire should be 0 when no IPVA date is set",
        )

    def test_compute_ipva_expiry_state_valid(self):
        """Test IPVA state computation for valid IPVA (more than 30 days)."""
        self.assertEqual(
            self.vehicle_valid.ipva_expiry_state,
            "valid",
            "IPVA state should be 'valid' for vehicle with more than 30 days",
        )

    def test_compute_ipva_expiry_state_expiring_soon(self):
        """Test IPVA state computation for IPVA expiring soon (less than 30 days)."""
        self.assertEqual(
            self.vehicle_expiring_soon.ipva_expiry_state,
            "expiring_soon",
            "IPVA state should be 'expiring_soon' for vehicle with 15 days",
        )

    def test_compute_ipva_expiry_state_expiring_30(self):
        """Test IPVA state computation for IPVA expiring in exactly 30 days."""
        self.assertEqual(
            self.vehicle_expiring_30.ipva_expiry_state,
            "expiring_soon",
            "IPVA state should be 'expiring_soon' for vehicle with exactly 30 days",
        )

    def test_compute_ipva_expiry_state_expiring_today(self):
        """Test IPVA state computation for IPVA expiring today."""
        self.assertEqual(
            self.vehicle_expiring_today.ipva_expiry_state,
            "expiring_soon",
            "IPVA state should be 'expiring_soon' for vehicle expiring today",
        )

    def test_compute_ipva_expiry_state_expired(self):
        """Test IPVA state computation for expired IPVA."""
        self.assertEqual(
            self.vehicle_expired.ipva_expiry_state,
            "expired",
            "IPVA state should be 'expired' for vehicle with negative days",
        )

    def test_compute_ipva_expiry_state_no_ipva(self):
        """Test IPVA state computation when no IPVA date is set."""
        self.assertEqual(
            self.vehicle_no_ipva.ipva_expiry_state,
            "no_ipva",
            "IPVA state should be 'no_ipva' when no date is set",
        )

    def test_update_ipva_date_triggers_recompute(self):
        """Test that updating IPVA date triggers recomputation of fields."""
        # Create a new vehicle
        vehicle = self.env["fleet.vehicle"].create(
            {
                "name": "Test Vehicle Update",
                "model_id": self.vehicle_model.id,
                "ipva_expiry_date": self.today + timedelta(days=100),
            }
        )

        # Verify initial state
        self.assertEqual(vehicle.ipva_days_to_expire, 100)
        self.assertEqual(vehicle.ipva_expiry_state, "valid")

        # Update IPVA date to expiring soon
        vehicle.write({"ipva_expiry_date": self.today + timedelta(days=20)})

        # Verify recomputation
        self.assertEqual(vehicle.ipva_days_to_expire, 20)
        self.assertEqual(vehicle.ipva_expiry_state, "expiring_soon")

        # Update IPVA date to expired
        vehicle.write({"ipva_expiry_date": self.today - timedelta(days=5)})

        # Verify recomputation
        self.assertEqual(vehicle.ipva_days_to_expire, -5)
        self.assertEqual(vehicle.ipva_expiry_state, "expired")

        # Remove IPVA date
        vehicle.write({"ipva_expiry_date": False})

        # Verify recomputation
        self.assertEqual(vehicle.ipva_days_to_expire, 0)
        self.assertEqual(vehicle.ipva_expiry_state, "no_ipva")

    def test_boundary_condition_31_days(self):
        """Test boundary condition: 31 days should be 'valid'."""
        vehicle = self.env["fleet.vehicle"].create(
            {
                "name": "Vehicle 31 Days",
                "model_id": self.vehicle_model.id,
                "ipva_expiry_date": self.today + timedelta(days=31),
            }
        )

        self.assertEqual(vehicle.ipva_days_to_expire, 31)
        self.assertEqual(
            vehicle.ipva_expiry_state,
            "valid",
            "IPVA state should be 'valid' for 31 days",
        )

    def test_boundary_condition_minus_1_day(self):
        """Test boundary condition: -1 day should be 'expired'."""
        vehicle = self.env["fleet.vehicle"].create(
            {
                "name": "Vehicle -1 Day",
                "model_id": self.vehicle_model.id,
                "ipva_expiry_date": self.today - timedelta(days=1),
            }
        )

        self.assertEqual(vehicle.ipva_days_to_expire, -1)
        self.assertEqual(
            vehicle.ipva_expiry_state,
            "expired",
            "IPVA state should be 'expired' for -1 day",
        )

    def test_multiple_vehicles_computation(self):
        """Test that computation works correctly for multiple vehicles at once."""
        vehicles = self.env["fleet.vehicle"].browse(
            [
                self.vehicle_valid.id,
                self.vehicle_expiring_soon.id,
                self.vehicle_expired.id,
                self.vehicle_no_ipva.id,
            ]
        )

        # Force recomputation
        vehicles._compute_ipva_days_to_expire()

        # Verify all vehicles have correct values
        self.assertEqual(self.vehicle_valid.ipva_expiry_state, "valid")
        self.assertEqual(self.vehicle_expiring_soon.ipva_expiry_state, "expiring_soon")
        self.assertEqual(self.vehicle_expired.ipva_expiry_state, "expired")
        self.assertEqual(self.vehicle_no_ipva.ipva_expiry_state, "no_ipva")
