from odoo import models, fields


class ImportedInventory(models.Model):
    """
    Stores a snapshot of an inventory imported from the external
    Inventory Management application.
    """
    _name = 'inventory.integration.imported_inventory'
    _description = 'Imported Inventory'
    _order = 'last_imported desc'

    # ── Identity ──────────────────────────────────────────────────────────────

    name = fields.Char(
        string='Inventory Title',
        required=True,
        readonly=True,
    )
    external_id = fields.Integer(
        string='External ID',
        readonly=True,
        help='Primary key of the inventory in the Inventory Management app.',
    )
    description = fields.Text(
        string='Description',
        readonly=True,
    )

    # ── API connection ────────────────────────────────────────────────────────

    api_url = fields.Char(
        string='API URL',
        required=True,
        help='Base URL of the Inventory Management app, e.g. https://my-app.onrender.com',
    )
    api_token = fields.Char(
        string='API Token',
        required=True,
        help='Per-inventory token generated in the Inventory Management app.',
    )

    # ── Aggregated summary ────────────────────────────────────────────────────

    item_count = fields.Integer(
        string='Total Items',
        readonly=True,
    )
    field_count = fields.Integer(
        string='Number of Fields',
        compute='_compute_field_count',
        store=True,
    )
    last_imported = fields.Datetime(
        string='Last Imported',
        readonly=True,
    )

    # ── Relations ─────────────────────────────────────────────────────────────

    field_ids = fields.One2many(
        comodel_name='inventory.integration.imported_field',
        inverse_name='inventory_id',
        string='Fields',
        readonly=True,
    )

    # ── Computed ──────────────────────────────────────────────────────────────

    def _compute_field_count(self):
        for rec in self:
            rec.field_count = len(rec.field_ids)

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_import(self):
        """Open the import wizard pre-filled with this record's connection info."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Inventory',
            'res_model': 'inventory.integration.import_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_api_url': self.api_url,
                'default_api_token': self.api_token,
                'default_inventory_id': self.id,
            },
        }
