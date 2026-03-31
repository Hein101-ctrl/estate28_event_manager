frappe.pages['estate28-dashboard'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Estate28 Dashboard',
        single_column: true
    });

    const $body = $(`
        <div class="estate28-dashboard">
            <div class="row" id="summary-cards" style="margin-bottom: 20px;"></div>
            <div class="row">
                <div class="col-md-6">
                    <div class="frappe-card" style="padding: 16px; margin-bottom: 20px;">
                        <h4>Upcoming Weddings</h4>
                        <div id="upcoming-weddings"></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="frappe-card" style="padding: 16px; margin-bottom: 20px;">
                        <h4>Outstanding Amounts</h4>
                        <div id="outstanding-amounts"></div>
                    </div>
                </div>
            </div>
            <div class="frappe-card" style="padding: 16px;">
                <h4>Photographer Cards</h4>
                <div class="row" id="photographer-cards"></div>
            </div>
        </div>
    `).appendTo(page.body);

    function currency(val) {
        const num = flt(val || 0);
        return format_currency(num);
    }

    function renderSummary(data) {
        const cards = [
            ['Total Weddings', data.total_weddings || 0],
            ['Upcoming 30 Days', data.upcoming_30_days || 0],
            ['Outstanding Total', currency(data.outstanding_total || 0)],
            ['Overdue Payments', data.overdue_payments || 0],
            ['Booked / Active', data.booked_count || 0]
        ];
        const html = cards.map(([label, value]) => `
            <div class="col-md-2">
                <div class="frappe-card" style="padding: 16px; margin-bottom: 12px;">
                    <div style="font-size: 12px; color: var(--text-muted);">${label}</div>
                    <div style="font-size: 24px; font-weight: 700;">${value}</div>
                </div>
            </div>
        `).join('');
        $body.find('#summary-cards').html(html);
    }

    function renderUpcoming(rows) {
        const html = rows.length ? rows.map(r => `
            <div class="frappe-card" style="padding: 12px; margin-bottom: 10px;">
                <div style="font-weight: 700;">${frappe.utils.escape_html(r.client_name || r.name)}</div>
                <div>${frappe.datetime.str_to_user(r.event_date || '')}</div>
                <div>${frappe.utils.escape_html(r.package_label || '')}</div>
                <div>Photographer: ${frappe.utils.escape_html(r.photographer || 'Unassigned')}</div>
                <div>DJ: ${frappe.utils.escape_html(r.dj || 'Unassigned')}</div>
                <div>Outstanding: ${currency(r.balance_due || 0)}</div>
            </div>
        `).join('') : '<div class="text-muted">No upcoming weddings found.</div>';
        $body.find('#upcoming-weddings').html(html);
    }

    function renderOutstanding(rows) {
        const html = rows.length ? rows.map(r => `
            <div class="frappe-card" style="padding: 12px; margin-bottom: 10px;">
                <div style="font-weight: 700;">${frappe.utils.escape_html(r.client_name || r.name)}</div>
                <div>Total: ${currency(r.total_amount || 0)}</div>
                <div>Paid: ${currency(r.amount_paid || 0)}</div>
                <div>Balance: ${currency(r.balance_due || 0)}</div>
                <div>Final payment: ${r.final_payment_date ? frappe.datetime.str_to_user(r.final_payment_date) : ''}</div>
            </div>
        `).join('') : '<div class="text-muted">No outstanding amounts found.</div>';
        $body.find('#outstanding-amounts').html(html);
    }

    function renderPhotographers(rows) {
        const html = rows.length ? rows.map(r => `
            <div class="col-md-3">
                <div class="frappe-card" style="padding: 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700;">${frappe.utils.escape_html(r.photographer || 'Unassigned')}</div>
                    <div>Upcoming weddings: ${r.upcoming_weddings || 0}</div>
                    <div>Next wedding: ${r.next_wedding_date ? frappe.datetime.str_to_user(r.next_wedding_date) : ''}</div>
                    <div>Next client: ${frappe.utils.escape_html(r.next_client || '')}</div>
                    <div>Outstanding total: ${currency(r.outstanding_total || 0)}</div>
                </div>
            </div>
        `).join('') : '<div class="col-md-12 text-muted">No photographer data found.</div>';
        $body.find('#photographer-cards').html(html);
    }

    frappe.call('estate28_event_manager.api.get_dashboard_summary').then(r => renderSummary(r.message || {}));
    frappe.call('estate28_event_manager.api.get_upcoming_weddings', {limit: 10}).then(r => renderUpcoming(r.message || []));
    frappe.call('estate28_event_manager.api.get_outstanding_amounts', {limit: 10}).then(r => renderOutstanding(r.message || []));
    frappe.call('estate28_event_manager.api.get_photographer_cards').then(r => renderPhotographers(r.message || []));
};
