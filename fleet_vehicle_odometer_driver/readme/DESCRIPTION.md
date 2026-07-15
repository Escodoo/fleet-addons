This module changes the `driver_id` field of the odometer log
(`fleet.vehicle.odometer`) from a related field pointing to the vehicle's
current driver into a stored, persisted field.

In standard Fleet, `driver_id` is `related="vehicle_id.driver_id"`, so whenever
the vehicle's driver changes, every odometer log (including historical ones)
reflects the new driver. This module freezes the driver on each log at creation
time:

- If the driver is sent in the `create` payload, that value is saved and kept.
- Otherwise, the log defaults to the vehicle's current driver at creation time.
