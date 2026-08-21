# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.tests import common


class TestFuelStockConsume(common.TransactionCase):
    """Test suite for fuel_stock_consume module.

    Covers field definitions, validation constraints, location routing,
    automatic odometer record creation, wizard flow, and analytic distribution
    for fuel consumption operations.
    """

    def setUp(self):
        """Set up test data for fuel consumption tests.

        Creates necessary test records including:
        - Stock locations (fuel consumption destination, internal source)
        - Picking types (fuel consumption, regular)
        - Fleet vehicles (with and without fuel location)
        - Stock products and partners
        - Initial stock in internal_location for wizard tests
        """
        super().setUp()

        self.company = self.env.company

        self.warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.company.id)], limit=1
        )
        if not self.warehouse:  # pragma: no cover
            self.warehouse = self.env["stock.warehouse"].create(
                {
                    "name": "Test Warehouse",
                    "company_id": self.company.id,
                    "code": "TEST",
                }
            )

        self.fuel_location = self.env["stock.location"].create(
            {
                "name": "Fuel Consumption",
                "usage": "inventory",
                "company_id": self.company.id,
            }
        )

        self.internal_location = self.env["stock.location"].create(
            {
                "name": "Internal Fuel Location",
                "usage": "internal",
                "company_id": self.company.id,
                "is_fuel_consumption_source": True,
            }
        )

        self.fuel_picking_type = self.env["stock.picking.type"].create(
            {
                "name": "Fuel Consumption",
                "code": "internal",
                "sequence": 1,
                "sequence_code": "INT-001",
                "warehouse_id": self.warehouse.id,
                "is_fuel_consumption": True,
                "default_location_src_id": self.internal_location.id,
                "default_location_dest_id": self.fuel_location.id,
            }
        )

        self.regular_picking_type = self.env["stock.picking.type"].create(
            {
                "name": "Regular Transfer",
                "code": "internal",
                "sequence": 2,
                "sequence_code": "INT-002",
                "warehouse_id": self.warehouse.id,
                "is_fuel_consumption": False,
                "default_location_src_id": self.warehouse.lot_stock_id.id,
                "default_location_dest_id": self.warehouse.lot_stock_id.id,
            }
        )

        self.vehicle_model = self.env["fleet.vehicle.model"].create(
            {
                "name": "Test Model",
                "brand_id": self.env["fleet.vehicle.model.brand"]
                .create({"name": "Test Brand"})
                .id,
            }
        )

        self.vehicle = self.env["fleet.vehicle"].create(
            {
                "name": "Test Vehicle",
                "license_plate": "ABC-1234",
                "model_id": self.vehicle_model.id,
                "fuel_consumption_location_id": self.fuel_location.id,
            }
        )

        self.vehicle_no_location = self.env["fleet.vehicle"].create(
            {
                "name": "Vehicle No Location",
                "license_plate": "XYZ-5678",
                "model_id": self.vehicle_model.id,
            }
        )

        self.fuel_product = self.env["product.product"].create(
            {
                "name": "Diesel Fuel",
                "type": "product",
                "categ_id": self.env.ref("product.product_category_all").id,
            }
        )

        self.driver = self.env["res.partner"].create(
            {
                "name": "John Driver",
            }
        )

        self.env["stock.quant"]._update_available_quantity(
            self.fuel_product, self.internal_location, 100.0
        )

    # -------------------------------------------------------------------------
    # Existing tests — stock.picking form-based flow
    # -------------------------------------------------------------------------

    def test_01_model_fields_existence(self):
        """Verify that all required fields exist in models.

        Tests that:
        - Picking type has is_fuel_consumption field
        - Vehicle has fuel_consumption_location_id field
        - Fields are correctly populated
        """
        self.assertTrue(
            hasattr(self.fuel_picking_type, "is_fuel_consumption"),
            "Picking type should have is_fuel_consumption field",
        )
        self.assertTrue(self.fuel_picking_type.is_fuel_consumption)
        self.assertFalse(self.regular_picking_type.is_fuel_consumption)

        self.assertTrue(
            hasattr(self.vehicle, "fuel_consumption_location_id"),
            "Vehicle should have fuel_consumption_location_id field",
        )
        self.assertEqual(self.vehicle.fuel_consumption_location_id, self.fuel_location)

    def test_02_draft_creation_without_vehicle(self):
        """Test fuel consumption picking can be created in draft without vehicle.

        Tests that:
        - Fuel consumption picking can be created in draft WITHOUT vehicle/odometer
        - ValidationError is raised ONLY when validating without required fields
        - Picking type is correctly identified as fuel consumption
        """
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )
        self.assertEqual(picking.state, "draft")
        self.assertFalse(picking.vehicle_id)
        self.assertFalse(picking.odometer_value)
        self.assertTrue(picking.picking_type_is_fuel_consumption)

    def test_03_validation_requires_vehicle_and_odometer(self):
        """Test validation at button_validate requires vehicle and odometer."""
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )
        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty

        with self.assertRaises(ValidationError):
            picking.button_validate()

        picking.vehicle_id = self.vehicle.id
        with self.assertRaises(ValidationError):
            picking.button_validate()

    def test_04_odometer_value_must_increase(self):
        """Test odometer value must be greater than last recorded."""
        self.env["fleet.vehicle.odometer"].create(
            {"vehicle_id": self.vehicle.id, "value": 100.0}
        )

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
                "vehicle_id": self.vehicle.id,
                "odometer_value": 50.0,
            }
        )
        self.assertTrue(picking.odometer_value == 50.0)  # can create with low value

        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )
        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty

        with self.assertRaises(ValidationError):
            picking.button_validate()

    def test_05_location_routing_with_vehicle_location(self):
        """Test location routing uses vehicle's fuel_consumption_location_id."""
        other_dest = self.env["stock.location"].create(
            {"name": "Other Dest", "usage": "inventory"}
        )
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": other_dest.id,
                "vehicle_id": self.vehicle.id,
                "odometer_value": 200.0,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": other_dest.id,
            }
        )
        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()

        for move in picking.move_ids:
            self.assertEqual(
                move.location_dest_id, self.vehicle.fuel_consumption_location_id
            )

    def test_06_location_routing_fallback(self):
        """Test location routing falls back to picking type default."""
        other_dest = self.env["stock.location"].create(
            {"name": "Other Dest 2", "usage": "inventory"}
        )
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": other_dest.id,
                "vehicle_id": self.vehicle_no_location.id,
                "odometer_value": 300.0,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": other_dest.id,
            }
        )
        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()

        for move in picking.move_ids:
            self.assertEqual(
                move.location_dest_id, self.fuel_picking_type.default_location_dest_id
            )

    def test_07_odometer_record_created(self):
        """Test odometer record is created with full traceability."""
        picking = self._create_and_validate_picking(
            odometer_value=400.0, driver=self.driver
        )

        odometer = self.env["fleet.vehicle.odometer"].search(
            [("stock_picking_id", "=", picking.id)]
        )
        self.assertEqual(len(odometer), 1)
        self.assertEqual(odometer.vehicle_id, self.vehicle)
        self.assertEqual(odometer.value, 400.0)
        self.assertEqual(odometer.driver_id, self.driver)
        self.assertEqual(odometer.stock_picking_id, picking)

    def test_08_no_duplicate_odometer(self):
        """Test duplicate odometer is not created."""
        picking = self._create_and_validate_picking(odometer_value=500.0)

        odometers_before = self.env["fleet.vehicle.odometer"].search_count(
            [("stock_picking_id", "=", picking.id)]
        )
        self.assertEqual(odometers_before, 1)

    def test_09_non_fuel_operations_unaffected(self):
        """Test that regular pickings are unaffected by fuel module.

        Tests that:
        - Non-fuel pickings can be created without vehicle_id
        - Non-fuel pickings can be validated without odometer_value
        - Regular operations work independently from fuel logic
        """
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.regular_picking_type.id,
                "location_id": self.warehouse.lot_stock_id.id,
                "location_dest_id": self.warehouse.lot_stock_id.id,
            }
        )

        self.env["stock.move"].create(
            {
                "name": "Regular Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.warehouse.lot_stock_id.id,
                "location_dest_id": self.warehouse.lot_stock_id.id,
            }
        )

        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()

        self.assertEqual(picking.state, "done")

    # -------------------------------------------------------------------------
    # New tests — stock.location, stock.move related fields
    # -------------------------------------------------------------------------

    def test_10_stock_location_fuel_source_field(self):
        """Test is_fuel_consumption_source field on stock.location."""
        self.assertTrue(
            hasattr(self.internal_location, "is_fuel_consumption_source"),
            "stock.location should have is_fuel_consumption_source field",
        )
        self.assertTrue(self.internal_location.is_fuel_consumption_source)
        self.assertFalse(self.fuel_location.is_fuel_consumption_source)

        non_source = self.env["stock.location"].create(
            {"name": "Non Source", "usage": "internal"}
        )
        self.assertFalse(non_source.is_fuel_consumption_source)

    def test_11_stock_move_vehicle_driver_related_fields(self):
        """Test vehicle_id and driver_id related fields on stock.move."""
        picking = self._create_and_validate_picking(
            odometer_value=600.0, driver=self.driver
        )
        self.assertTrue(picking.move_ids)
        for move in picking.move_ids:
            self.assertEqual(
                move.vehicle_id,
                self.vehicle,
                "stock.move.vehicle_id should be related from picking",
            )
            self.assertEqual(
                move.driver_id,
                self.driver,
                "stock.move.driver_id should be related from picking",
            )

    def test_12_stock_move_no_vehicle_when_not_set(self):
        """Test stock.move vehicle_id is empty for regular pickings."""
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.regular_picking_type.id,
                "location_id": self.warehouse.lot_stock_id.id,
                "location_dest_id": self.warehouse.lot_stock_id.id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "name": "Regular Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 5,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.warehouse.lot_stock_id.id,
                "location_dest_id": self.warehouse.lot_stock_id.id,
            }
        )
        self.assertFalse(move.vehicle_id)
        self.assertFalse(move.driver_id)

    # -------------------------------------------------------------------------
    # New tests — analytic_distribution on stock.picking
    # -------------------------------------------------------------------------

    def test_13_analytic_distribution_field_on_picking(self):
        """Test analytic_distribution field exists on stock.picking."""
        self.assertIn(
            "analytic_distribution",
            self.env["stock.picking"]._fields,
            "stock.picking should have analytic_distribution field",
        )
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
                "vehicle_id": self.vehicle.id,
                "odometer_value": 700.0,
                "analytic_distribution": {"999": 100.0},
            }
        )
        self.assertEqual(picking.analytic_distribution, {"999": 100.0})

    def test_14_analytic_distribution_propagation_runs_without_error(self):
        """Test _propagate_analytic_distribution executes without error.

        Since analytic_distribution on stock.move depends on stock_account,
        we verify the propagation logic handles its presence or absence gracefully.
        """
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
                "vehicle_id": self.vehicle.id,
                "odometer_value": 800.0,
                "analytic_distribution": {"999": 100.0},
            }
        )
        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )
        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()

        self.assertEqual(picking.state, "done")
        if "analytic_distribution" in self.env["stock.move"]._fields:
            for move in picking.move_ids:
                self.assertEqual(move.analytic_distribution, {"999": 100.0})

    # -------------------------------------------------------------------------
    # New tests — fuel.consume.wizard (main wizard)
    # -------------------------------------------------------------------------

    def test_15_fuel_consume_wizard_creation(self):
        """Test fuel.consume.wizard can be created with all required fields."""
        wizard = self._create_fuel_wizard(odometer_value=1000.0)
        self.assertEqual(wizard.vehicle_id, self.vehicle)
        self.assertEqual(wizard.driver_id, self.driver)
        self.assertEqual(wizard.odometer_value, 1000.0)
        self.assertEqual(wizard.location_id, self.internal_location)
        self.assertEqual(wizard.picking_type_id, self.fuel_picking_type)
        self.assertEqual(wizard.product_id, self.fuel_product)
        self.assertEqual(wizard.product_uom_qty, 10.0)

    def test_16_fuel_consume_wizard_available_qty(self):
        """Test available_qty is computed from stock.quant at source location."""
        wizard = self._create_fuel_wizard(odometer_value=1100.0)
        self.assertGreater(
            wizard.available_qty,
            0,
            "Available qty should reflect the 100 units added in setUp",
        )
        self.assertAlmostEqual(wizard.available_qty, 100.0, places=2)

    def test_17_fuel_consume_wizard_available_qty_zero_empty_location(self):
        """Test available_qty is 0 when source location holds no stock."""
        empty_source = self.env["stock.location"].create(
            {
                "name": "Empty Fuel Source",
                "usage": "internal",
                "is_fuel_consumption_source": True,
            }
        )
        wizard = self.env["fuel.consume.wizard"].create(
            {
                "vehicle_id": self.vehicle.id,
                "odometer_value": 1200.0,
                "location_id": empty_source.id,
                "picking_type_id": self.fuel_picking_type.id,
                "product_id": self.fuel_product.id,
                "product_uom_id": self.fuel_product.uom_id.id,
                "product_uom_qty": 10.0,
            }
        )
        self.assertAlmostEqual(wizard.available_qty, 0.0, places=2)

    def test_18_fuel_consume_wizard_action_next_opens_confirm(self):
        """Test action_next creates confirm wizard and returns correct action."""
        wizard = self._create_fuel_wizard(odometer_value=1300.0)
        result = wizard.action_next()

        self.assertEqual(result["type"], "ir.actions.act_window")
        self.assertEqual(result["res_model"], "fuel.consume.confirm.wizard")
        self.assertEqual(result["target"], "new")

        confirm = self.env["fuel.consume.confirm.wizard"].browse(result["res_id"])
        self.assertTrue(confirm.exists())
        self.assertEqual(confirm.vehicle_id, wizard.vehicle_id)
        self.assertEqual(confirm.driver_id, wizard.driver_id)
        self.assertEqual(confirm.odometer_value, wizard.odometer_value)
        self.assertEqual(confirm.location_id, wizard.location_id)
        self.assertEqual(confirm.picking_type_id, wizard.picking_type_id)
        self.assertEqual(confirm.product_id, wizard.product_id)
        self.assertEqual(confirm.product_uom_qty, wizard.product_uom_qty)

    def test_19_fuel_consume_wizard_action_next_transfers_analytic(self):
        """Test action_next passes analytic_distribution to confirm wizard."""
        analytic_data = {"42": 60.0, "43": 40.0}
        wizard = self._create_fuel_wizard(odometer_value=1400.0)
        wizard.analytic_distribution = analytic_data
        result = wizard.action_next()

        confirm = self.env["fuel.consume.confirm.wizard"].browse(result["res_id"])
        self.assertEqual(confirm.analytic_distribution, analytic_data)

    def test_20_fuel_consume_wizard_zero_qty_raises(self):
        """Test action_next raises ValidationError when quantity is zero."""
        wizard = self._create_fuel_wizard(odometer_value=1500.0, qty=0.0)
        with self.assertRaises(ValidationError):
            wizard.action_next()

    # -------------------------------------------------------------------------
    # New tests — fuel.consume.confirm.wizard
    # -------------------------------------------------------------------------

    def test_21_fuel_consume_confirm_creates_and_validates_picking(self):
        """Test action_confirm creates a fuel consumption picking in state done."""
        confirm = self._get_confirm_wizard(odometer_value=1600.0)
        confirm.action_confirm()

        picking = self.env["stock.picking"].search(
            [
                ("vehicle_id", "=", self.vehicle.id),
                ("picking_type_id", "=", self.fuel_picking_type.id),
                ("state", "=", "done"),
            ],
            order="id desc",
            limit=1,
        )
        self.assertTrue(picking, "A done picking should have been created")
        self.assertEqual(picking.location_id, self.internal_location)
        self.assertEqual(picking.location_dest_id, self.fuel_location)
        self.assertEqual(picking.odometer_value, 1600.0)

    def test_22_fuel_consume_confirm_creates_odometer_record(self):
        """Test action_confirm triggers odometer record creation."""
        confirm = self._get_confirm_wizard(odometer_value=1700.0)
        confirm.action_confirm()

        picking = self.env["stock.picking"].search(
            [
                ("vehicle_id", "=", self.vehicle.id),
                ("state", "=", "done"),
                ("odometer_value", "=", 1700.0),
            ],
            limit=1,
        )
        self.assertTrue(picking)
        odometer = self.env["fleet.vehicle.odometer"].search(
            [("stock_picking_id", "=", picking.id)]
        )
        self.assertEqual(len(odometer), 1)
        self.assertEqual(odometer.value, 1700.0)
        self.assertEqual(odometer.vehicle_id, self.vehicle)

    def test_23_fuel_consume_confirm_returns_close_action(self):
        """Test action_confirm returns act_window_close without opening picking."""
        confirm = self._get_confirm_wizard(odometer_value=1800.0)
        result = confirm.action_confirm()
        self.assertEqual(
            result,
            {"type": "ir.actions.act_window_close"},
            "Confirm wizard should close without opening the generated picking",
        )

    def test_24_fuel_consume_confirm_propagates_analytic(self):
        """Test action_confirm propagates analytic_distribution to the picking."""
        analytic_data = {"10": 100.0}
        wizard = self._create_fuel_wizard(odometer_value=1900.0)
        wizard.analytic_distribution = analytic_data
        result = wizard.action_next()
        confirm = self.env["fuel.consume.confirm.wizard"].browse(result["res_id"])
        confirm.action_confirm()

        picking = self.env["stock.picking"].search(
            [
                ("vehicle_id", "=", self.vehicle.id),
                ("state", "=", "done"),
                ("odometer_value", "=", 1900.0),
            ],
            limit=1,
        )
        self.assertTrue(picking)
        self.assertEqual(picking.analytic_distribution, analytic_data)

    def test_25_fuel_consume_confirm_insufficient_stock_raises(self):
        """Test action_confirm raises UserError when stock is insufficient."""
        confirm = self._get_confirm_wizard(odometer_value=2000.0, qty=9999.0)
        with self.assertRaises(UserError):
            confirm.action_confirm()

    def test_26_fuel_consume_confirm_no_dest_location_raises(self):
        """Test action_confirm raises UserError when no dest location configured."""
        confirm = self._get_confirm_wizard(
            odometer_value=2100.0, vehicle=self.vehicle_no_location
        )
        self.fuel_picking_type.default_location_dest_id = False
        with self.assertRaises(UserError):
            confirm.action_confirm()

    # -------------------------------------------------------------------------
    # New tests — stock moves smart button on fleet.vehicle
    # -------------------------------------------------------------------------

    def test_27_vehicle_stock_move_count(self):
        """Test stock_move_count counts only the moves of each vehicle."""
        self.assertEqual(self.vehicle.stock_move_count, 0)
        self.assertEqual(self.vehicle_no_location.stock_move_count, 0)

        picking = self._create_and_validate_picking(odometer_value=2200.0)

        self.vehicle.invalidate_recordset(["stock_move_count"])
        self.assertEqual(self.vehicle.stock_move_count, len(picking.move_ids))
        self.assertEqual(self.vehicle.stock_move_ids, picking.move_ids)
        self.assertEqual(self.vehicle_no_location.stock_move_count, 0)

    def test_28_vehicle_action_view_stock_moves(self):
        """Test action_view_stock_moves returns the moves of the vehicle."""
        picking = self._create_and_validate_picking(odometer_value=2300.0)

        action = self.vehicle.action_view_stock_moves()
        self.assertEqual(action["res_model"], "stock.move")
        self.assertEqual(action["domain"], [("vehicle_id", "=", self.vehicle.id)])

        moves = self.env["stock.move"].search(action["domain"])
        self.assertEqual(moves, picking.move_ids)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _create_fuel_wizard(self, odometer_value, qty=10.0, vehicle=None):
        """Create a fuel.consume.wizard with default test values."""
        return self.env["fuel.consume.wizard"].create(
            {
                "vehicle_id": (vehicle or self.vehicle).id,
                "driver_id": self.driver.id,
                "odometer_value": odometer_value,
                "location_id": self.internal_location.id,
                "picking_type_id": self.fuel_picking_type.id,
                "product_id": self.fuel_product.id,
                "product_uom_id": self.fuel_product.uom_id.id,
                "product_uom_qty": qty,
            }
        )

    def _get_confirm_wizard(self, odometer_value, qty=10.0, vehicle=None):
        """Create main wizard and return the resulting confirm wizard."""
        wizard = self._create_fuel_wizard(
            odometer_value=odometer_value, qty=qty, vehicle=vehicle
        )
        if qty > 0:
            result = wizard.action_next()
            return self.env["fuel.consume.confirm.wizard"].browse(result["res_id"])
        return wizard

    def _create_and_validate_picking(self, odometer_value, driver=None):
        """Helper to create and validate a fuel consumption picking.

        Returns the created picking after validation.
        """
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.fuel_picking_type.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
                "vehicle_id": self.vehicle.id,
                "odometer_value": odometer_value,
                "driver_id": driver.id if driver else False,
            }
        )

        self.env["stock.move"].create(
            {
                "name": "Fuel Move",
                "product_id": self.fuel_product.id,
                "product_uom_qty": 10,
                "product_uom": self.fuel_product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.internal_location.id,
                "location_dest_id": self.fuel_location.id,
            }
        )

        picking.action_confirm()
        for move in picking.move_ids:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()

        return picking
