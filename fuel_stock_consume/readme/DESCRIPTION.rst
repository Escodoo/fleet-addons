This module extends Odoo's stock management to enable fuel consumption tracking through inventory operations. When fuel is taken from stock for vehicle consumption, the system:

1. Requires vehicle identification and current odometer reading
2. Automatically records odometer readings in fleet.vehicle.odometer
3. Routes fuel movements to the correct location (vehicle-specific or default)
4. Creates audit trail linking stock movements to vehicle operations

Key Features:

- **Fuel Consumption Operation Type**: Mark specific picking types as fuel operations
- **Automatic Odometer Recording**: Creates vehicle odometer records with full traceability
- **Smart Location Routing**: Routes fuel to vehicle-specific or default consumption location
- **Validation Constraints**: Ensures vehicle data and monotonically increasing odometer values
- **Multi-Vehicle Support**: Handle fuel distribution to multiple vehicles in single picking
