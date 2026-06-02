from odoo import models, fields


class ImportedInventory(models.Model):
    _name = 'inventory.imported_inventory'
    _description = 'Imported Inventory'
    _order = 'imported_at desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    item_count = fields.Integer(string='Item Count')
    imported_at = fields.Datetime(string='Imported At', default=fields.Datetime.now)

    field_ids = fields.One2many(
        'inventory.imported_field', 'inventory_id', string='Fields'
    )


class ImportedField(models.Model):
    _name = 'inventory.imported_field'
    _description = 'Imported Inventory Field'

    inventory_id = fields.Many2one(
        'inventory.imported_inventory', string='Inventory',
        required=True, ondelete='cascade'
    )
    name = fields.Char(string='Field Name', required=True)
    field_type = fields.Char(string='Type')
    slot = fields.Char(string='Slot')

    total_items = fields.Integer(string='Total Items')
    filled_count = fields.Integer(string='Filled')
    fill_percent = fields.Integer(string='Fill %')

    # Number stats
    num_min = fields.Float(string='Min', digits=(16, 4))
    num_max = fields.Float(string='Max', digits=(16, 4))
    num_avg = fields.Float(string='Avg', digits=(16, 4))

    # Bool stats
    bool_true_count = fields.Integer(string='True')
    bool_false_count = fields.Integer(string='False')
    bool_null_count = fields.Integer(string='Null')

    # Top values (stored as plain text: "val1(3), val2(2)")
    top_values = fields.Text(string='Top Values')
