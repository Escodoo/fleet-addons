# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, new_test_user


class TestFleetPreventiveMaintenance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager = new_test_user(
            cls.env, login="fleet_manager", groups="fleet.fleet_group_manager"
        )
        cls.user = new_test_user(
            cls.env, login="fleet_user", groups="fleet.fleet_group_user"
        )
        cls.brand = cls.env["fleet.vehicle.model.brand"].create({"name": "Test Brand"})
        cls.model = cls.env["fleet.vehicle.model"].create(
            {
                "name": "Test Model",
                "brand_id": cls.brand.id,
                "preventive_interval": 10000.0,
            }
        )
        cls.vehicle = cls.env["fleet.vehicle"].create(
            {
                "model_id": cls.model.id,
                "license_plate": "TEST0001",
                "manager_id": cls.manager.id,
            }
        )

    def _add_odometer(self, value, user=None):
        model = self.env["fleet.vehicle.odometer"]
        if user:
            model = model.with_user(user)
        return model.create({"vehicle_id": self.vehicle.id, "value": value})

    def test_01_no_alert_below_interval(self):
        """Readings below the interval do not raise an alert."""
        self._add_odometer(9999.0)
        self.assertFalse(self.vehicle.preventive_maintenance_alert_ids)

    def test_02_alert_on_interval(self):
        """Reaching the interval raises one alert with the odometer value."""
        self._add_odometer(10000.0)
        alerts = self.vehicle.preventive_maintenance_alert_ids
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts.odometer_value, 10000.0)

    def test_03_next_alert_only_after_a_new_interval(self):
        """The interval is counted from the last alert, not from zero."""
        self._add_odometer(10000.0)
        self._add_odometer(15000.0)
        self.assertEqual(len(self.vehicle.preventive_maintenance_alert_ids), 1)
        self._add_odometer(20000.0)
        self.assertEqual(len(self.vehicle.preventive_maintenance_alert_ids), 2)

    def test_04_activity_assigned_to_the_manager(self):
        """The alert schedules an activity for the manager of the vehicle."""
        self._add_odometer(10000.0)
        alert = self.vehicle.preventive_maintenance_alert_ids
        self.assertTrue(alert.activity_id)
        self.assertEqual(alert.activity_id.user_id, self.manager)
        self.assertEqual(alert.activity_id.res_id, self.vehicle.id)

    def test_05_no_interval_no_alert(self):
        """Without an interval on the model the module stays out of the way."""
        self.model.preventive_interval = 0.0
        self._add_odometer(50000.0)
        self.assertFalse(self.vehicle.preventive_maintenance_alert_ids)

    def test_06_driver_can_register_an_odometer(self):
        """The driver of the vehicle is not blocked by the alert ACLs.

        A fleet user may create odometer readings for the vehicle they drive
        (``fleet_rule_odometer_visibility_user``), but the ACLs only give
        create on the alert to the fleet manager. So the alert has to be
        created with sudo(), otherwise the driver cannot register a reading
        that reaches the interval.
        """
        self.vehicle.driver_id = self.user.partner_id
        odometer = self._add_odometer(10000.0, user=self.user)
        self.assertTrue(odometer.exists())
        self.assertEqual(len(self.vehicle.preventive_maintenance_alert_ids), 1)

    def test_07_no_manager_no_activity(self):
        """Without a manager on the vehicle the alert is still created."""
        self.vehicle.manager_id = False
        self._add_odometer(10000.0)
        alert = self.vehicle.preventive_maintenance_alert_ids
        self.assertEqual(len(alert), 1)
        self.assertFalse(alert.activity_id)
