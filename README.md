# Estate28 Event Manager

Custom Frappe / ERPNext app for wedding and event planning at Estate28.

## What is included

- **Estate 28 Event** DocType
- **Create Customer** button logic
- **Create Sales Invoice** button logic
- helper methods to:
  - create a Customer if one does not exist
  - create a Sales Invoice linked to the event
  - auto-calculate final payment dates and event title
- import-ready CSV generated from uploaded 2026 wedding data

## Important

This is a practical starter app scaffold for Frappe Cloud / ERPNext v15 style setups.
After installation, review field labels, permissions, and item names inside ERPNext.

## Suggested ERPNext setup before using invoice generation

Create an Item in ERPNext:

- **Event Booking**
- or update the default item code in the app

The invoice tool uses the item code:
`Event Booking`

## GitHub / Frappe Cloud

At the **root** of the repository you must see:

- `pyproject.toml`
- `README.md`
- `estate28_event_manager/`

If `pyproject.toml` is nested one level down, Frappe Cloud will reject the app.


## Version 3 additions

- Safe update path from v1/v2 when no manual Customize Form changes were made
- Added Venue Area
- Added Deposit Amount, Amount Paid, Balance Due
- Added Internal Status for operational tracking
- Auto-calculates Balance Due from Package Amount minus Amount Paid
