from odoo import models, fields


class ImportedField(models.Model):
    """
    Stores one field definition together with its aggregated statistics
    for a single imported inventory snapshot.
    """
    _name = 'inventory.integration.imported_field'
    _description = 'Imported Inventory Field'
    _order = 'slot'

    inventory_id = fields.Many2one(
        comodel_name='inventory.integration.imported_inventory',
        string='Inventory',
        required=True,
        ondelete='cascade',
        readonly=True,
    )

    # ── Field definition ──────────────────────────────────────────────────────

    name = fields.Char(string='Field Name', readonly=True)
    field_type = fields.Selection(
        selection=[
            ('String',  'String'),
            ('Text',    'Text'),
            ('Link',    'Link'),
            ('Number',  'Number'),
            ('Bool',    'Boolean'),
        ],
        string='Type',
        readonly=True,
    )
    slot = fields.Char(
        string='Slot',
        readonly=True,
        help='Physical column in the Inventory Management DB, e.g. Number1, String2.',
    )

    # ── Fill rate ─────────────────────────────────────────────────────────────

    total_items  = fields.Integer(string='Total Items',   readonly=True)
    filled_count = fields.Integer(string='Filled Count',  readonly=True)
    fill_percent = fields.Integer(string='Fill %',        readonly=True)

    # ── Number stats ──────────────────────────────────────────────────────────

    num_min = fields.Float(string='Min',     readonly=True)
    num_max = fields.Float(string='Max',     readonly=True)
    num_avg = fields.Float(string='Average', readonly=True)

    # ── String / Text stats ───────────────────────────────────────────────────

    top_values = fields.Text(
        string='Top Values',
        readonly=True,
        help='Up to 5 most frequent values with their counts (JSON array).',
    )

    # ── Bool stats ────────────────────────────────────────────────────────────

    bool_true_count  = fields.Integer(string='True Count',  readonly=True)
    bool_false_count = fields.Integer(string='False Count', readonly=True)
    bool_null_count  = fields.Integer(string='Null Count',  readonly=True)
