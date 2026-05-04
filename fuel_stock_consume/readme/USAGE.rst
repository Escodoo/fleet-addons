Setup
=====

1. Configure Fuel Consumption Operation Type

   - Navigate to Inventory > Configuration > Operation Types
   - Create or edit a type for fuel operations
   - Check the "Fuel Consumption" checkbox
   - Set appropriate source/destination locations

2. Configure Vehicle Fuel Location

   - Navigate to Fleet > Vehicles
   - Edit the vehicle
   - Set "Fuel Consumption Location" to where fuel is consumed (e.g., Inventory Loss)
   - This is optional; if not set, picking type's default location is used

3. Prepare Fuel Products

   - Create storable fuel products (e.g., "Diesel Fuel", "Gasoline")
   - Ensure proper inventory accounts are configured


Basic Workflow
==============

1. Create an Internal Transfer with Fuel Consumption type
2. Select the vehicle being refueled
3. Enter current odometer reading (must be ≥ last recorded value)
4. Optionally assign a driver
5. Add fuel product line(s) with quantities
6. Confirm and validate

The system will:

- Automatically update move destination locations (vehicle location > picking type default)
- Create fleet.vehicle.odometer record with full traceability
- Decrease stock accordingly


Advanced Usage
==============

Multiple Vehicles in Single Picking

   - Add multiple move lines, one per vehicle
   - Fill vehicle and odometer for each line
   - All moves will be routed and tracked individually

Project Integration (Optional)

   - If using analytic accounts, assign fuel consumption to projects
   - Automatically creates analytical lines

Reporting

   - View fuel consumption history in Fleet > Vehicles > Odometer
   - Filter by date range, vehicle, or driver
   - Link back to source stock picking for audit trail
