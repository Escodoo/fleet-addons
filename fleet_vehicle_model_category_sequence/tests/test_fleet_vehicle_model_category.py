# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestFleetVehicleLogic(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_model = cls.env["fleet.vehicle.model.category"]
        cls.vehicle_model = cls.env["fleet.vehicle"]
        cls.fleet_model = cls.env["fleet.vehicle.model"]
        cls.brand_model = cls.env["fleet.vehicle.model.brand"]

        cls.brand = cls.brand_model.create({"name": "Brand X"})
        cls.model = cls.fleet_model.create(
            {
                "name": "Model X",
                "brand_id": cls.brand.id,
            }
        )

    def test_category_normalization_and_sequence_creation(self):
        """Tests if the code is normalized and the sequence is created on create"""
        category = self.category_model.create({"name": "Truck", "code": " tru "})

        self.assertEqual(
            category.code, "TRU", "The code should be uppercase and without spaces."
        )
        self.assertTrue(category.sequence_id, "The sequence should have been created.")
        self.assertEqual(
            category.sequence_id.prefix,
            "TRU",
            "The sequence prefix must be the category code.",
        )

    def test_category_write_sync(self):
        """Tests if the sequence is updated when the category is changed"""
        category = self.category_model.create({"name": "Car", "code": "CAR"})
        old_sequence_name = category.sequence_id.name

        category.write({"name": "Luxury Car", "code": "LUX"})

        self.assertEqual(category.code, "LUX")
        self.assertEqual(
            category.sequence_id.prefix,
            "LUX",
            "The sequence prefix should have been updated.",
        )
        self.assertNotEqual(
            category.sequence_id.name,
            old_sequence_name,
            "The sequence name should have changed.",
        )

    def test_vehicle_code_generation_on_create(self):
        """Tests if the vehicle receives the code automatically on creation"""
        category = self.category_model.create({"name": "Van", "code": "VAN"})

        vehicle = self.vehicle_model.create(
            {
                "model_id": self.model.id,
                "category_id": category.id,
                "license_plate": "ABC-1234",
            }
        )

        self.assertTrue(
            vehicle.code.startswith("VAN"),
            "The vehicle code must start with the category prefix.",
        )
        self.assertEqual(
            vehicle.code,
            "VAN1",
            "Since it's the first, the code should be VAN1 (padding 0).",
        )

    def test_vehicle_code_generation_on_write(self):
        """Tests if the vehicle code changes when the category is updated"""
        cat_a = self.category_model.create({"name": "A", "code": "AAA"})
        cat_b = self.category_model.create({"name": "B", "code": "BBB"})

        vehicle = self.vehicle_model.create(
            {
                "model_id": self.model.id,
                "category_id": cat_a.id,
                "license_plate": "PLATE-1",
            }
        )
        self.assertEqual(vehicle.code, "AAA1")

        vehicle.write({"category_id": cat_b.id})
        self.assertEqual(
            vehicle.code,
            "BBB1",
            "The code should have been regenerated with the new category.",
        )

    def test_create_multi_category(self):
        """Tests api.model_create_multi on category"""
        categories = self.category_model.create(
            [{"name": "Mult 1", "code": "m1"}, {"name": "Mult 2", "code": "m2"}]
        )
        self.assertEqual(categories[0].code, "M1")
        self.assertEqual(categories[1].code, "M2")
        self.assertTrue(categories[0].sequence_id)
        self.assertTrue(categories[1].sequence_id)

    def test_vehicle_without_category(self):
        """Tests vehicle created without category"""
        vehicle = self.vehicle_model.create(
            {"model_id": self.model.id, "license_plate": "NO-CAT"}
        )
        self.assertFalse(
            vehicle.code, "Vehicle without category should not have a generated code."
        )

    def test_vehicle_create_with_category_without_sequence(self):
        category = self.category_model.create(
            {
                "name": "No Seq",
                "code": "NSQ",
            }
        )
        category.write({"sequence_id": False})

        vehicle = self.vehicle_model.create(
            {
                "model_id": self.model.id,
                "category_id": category.id,
                "license_plate": "NOSEQ-1",
            }
        )
        self.assertFalse(vehicle.code)

    def test_vehicle_write_with_category_without_sequence(self):
        category = self.category_model.create(
            {
                "name": "No Seq Write",
                "code": "NSW",
            }
        )
        category.write({"sequence_id": False})

        vehicle = self.vehicle_model.create(
            {
                "model_id": self.model.id,
                "license_plate": "WRITE-1",
            }
        )
        vehicle.write({"category_id": category.id})
        self.assertFalse(vehicle.code)
