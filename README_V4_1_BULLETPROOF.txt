Estate28 Event Manager v4.1 Bulletproof

Purpose:
- Safe upgrade package after v4 migration failed on live data.

Why v4 failed:
- Existing rows in tabEstate 28 Event contain non-boolean values in fields such as wooden_benches.
- Frappe tried to convert those columns to Check/tinyint and MariaDB rejected the values.

What v4.1 changes:
- Keeps the dashboard, workspace, page and reports from v4
- Converts these risky fields to Small Text instead of Check:
  wooden_benches, speech_stand, confetti_stands, welcome_sign,
  gift_box, register_table, throw_bouquet, welcome_drink_table,
  seating_board, coffee_tea_station, barman, extra_barman

Result:
- Existing values should survive migration without Data truncated errors
- You still get the new Desk workspace, dashboard and reports

Deploy:
1. Replace the same GitHub repo contents with this package
2. Commit and push
3. Run the same Frappe Cloud deploy again

If a new migration error appears on a different field, that field should be treated the same way:
preserve the live data first, then normalize later.
