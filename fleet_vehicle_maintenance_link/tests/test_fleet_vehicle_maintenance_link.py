# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestFleetVehicleMaintenanceLink(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vehicle_model = cls.env["fleet.vehicle"]
        cls.equipment_model = cls.env["maintenance.equipment"]
        cls.request_model = cls.env["maintenance.request"]

        cls.team = cls.env["maintenance.team"].create({"name": "Test Maintenance Team"})
        cls.vehicle = cls.vehicle_model.create(
            {
                "model_id": cls.env.ref("fleet.model_astra").id,
                "license_plate": "MNT-0001",
            }
        )
        cls.other_vehicle = cls.vehicle_model.create(
            {
                "model_id": cls.env.ref("fleet.model_astra").id,
                "license_plate": "MNT-0002",
            }
        )

    def _create_equipment(self, vehicle=None, name="Equipment"):
        vals = {"name": name}
        if vehicle is not None:
            vals["fleet_vehicle_id"] = vehicle.id
        return self.equipment_model.create(vals)

    def _create_request(self, equipment, name="Request"):
        return self.request_model.create(
            {
                "name": name,
                "equipment_id": equipment.id,
                "maintenance_team_id": self.team.id,
            }
        )

    def test_fleet_vehicle_id_on_equipment(self):
        """Setting the vehicle on the equipment exposes it on both sides."""
        equipment = self._create_equipment(vehicle=self.vehicle)
        self.assertEqual(equipment.fleet_vehicle_id, self.vehicle)
        self.assertIn(equipment, self.vehicle.maintenance_equipment_ids)

    def test_equipment_without_vehicle(self):
        """Equipments are not required to have a vehicle."""
        equipment = self._create_equipment()
        self.assertFalse(equipment.fleet_vehicle_id)

    def test_maintenance_request_count_zero_without_equipment(self):
        """A vehicle with no linked equipment has zero maintenances."""
        self.assertEqual(self.vehicle.maintenance_request_count, 0)

    def test_maintenance_request_count_zero_without_requests(self):
        """Linking an equipment alone does not create maintenances."""
        self._create_equipment(vehicle=self.vehicle)
        self.assertEqual(self.vehicle.maintenance_request_count, 0)

    def test_maintenance_request_count_single(self):
        """A single request on the vehicle's equipment is counted."""
        equipment = self._create_equipment(vehicle=self.vehicle)
        self._create_request(equipment)
        self.assertEqual(self.vehicle.maintenance_request_count, 1)

    def test_maintenance_request_count_multiple_requests(self):
        """Several requests on the same equipment are all counted."""
        equipment = self._create_equipment(vehicle=self.vehicle)
        self._create_request(equipment, name="Request 1")
        self._create_request(equipment, name="Request 2")
        self.assertEqual(self.vehicle.maintenance_request_count, 2)

    def test_maintenance_request_count_multiple_equipments(self):
        """Requests on different equipments of the same vehicle are summed."""
        equipment_a = self._create_equipment(vehicle=self.vehicle, name="Equipment A")
        equipment_b = self._create_equipment(vehicle=self.vehicle, name="Equipment B")
        self._create_request(equipment_a)
        self._create_request(equipment_b)
        self.assertEqual(self.vehicle.maintenance_request_count, 2)

    def test_maintenance_request_count_does_not_leak_between_vehicles(self):
        """Each vehicle only counts its own equipments' requests."""
        own_equipment = self._create_equipment(vehicle=self.vehicle)
        other_equipment = self._create_equipment(vehicle=self.other_vehicle)
        self._create_request(own_equipment)
        self._create_request(other_equipment)
        self.assertEqual(self.vehicle.maintenance_request_count, 1)
        self.assertEqual(self.other_vehicle.maintenance_request_count, 1)

    def test_maintenance_request_count_ignores_equipment_without_vehicle(self):
        """Requests on equipments not linked to any vehicle are not counted."""
        equipment = self._create_equipment()
        self._create_request(equipment)
        self.assertEqual(self.vehicle.maintenance_request_count, 0)

    def test_action_view_maintenance_requests(self):
        """The smart button action targets exactly this vehicle's requests."""
        equipment = self._create_equipment(vehicle=self.vehicle)
        request = self._create_request(equipment)
        unrelated_equipment = self._create_equipment(vehicle=self.other_vehicle)
        self._create_request(unrelated_equipment)

        action = self.vehicle.action_view_maintenance_requests()

        self.assertEqual(action["res_model"], "maintenance.request")
        self.assertEqual(
            action["domain"],
            [("equipment_id.fleet_vehicle_id", "=", self.vehicle.id)],
        )
        self.assertEqual(self.request_model.search(action["domain"]), request)
