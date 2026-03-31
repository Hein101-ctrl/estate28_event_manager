Estate28 Event Manager v4 Clean

This package is a safe replacement for the earlier v4 build.

What changed:
- Uses v3 as the schema base
- Does NOT modify the Estate 28 Event DocType field types
- Adds:
  - Desk workspace: Estate28 Event Manager
  - Dashboard page: Estate28 Dashboard
  - Script reports:
    - Upcoming Weddings
    - Outstanding Amounts
    - Photographer Schedule
    - Weddings by Status
  - Helper API for dashboard summary/cards

Why this build exists:
- The earlier v4 attempted DocType changes that triggered migration errors on live data.
- This clean build avoids all DocType schema changes.

Patch method:
1. Use the same GitHub repo already linked to Frappe Cloud
2. Replace the repo contents with this package
3. Commit and push
4. Deploy the update to the same site

Expected result:
- Update should migrate cleanly because the DocType schema stays on the stable v3 definition.
- Workspace, dashboard and reports should appear after deploy.
