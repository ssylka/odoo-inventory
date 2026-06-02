import urllib.request
import urllib.error
import json

from odoo import models, fields, api
from odoo.exceptions import UserError


class ImportInventoryWizard(models.TransientModel):
    _name = 'inventory.import_wizard'
    _description = 'Import Inventory from API'

    api_url = fields.Char(
        string='API URL',
        default='https://inventory-management-njpx.onrender.com/api/inventory',
        required=True,
    )
    api_token = fields.Char(string='API Token', required=True)

    def action_import(self):
        url = f"{self.api_url.rstrip('/')}?token={self.api_token}"
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise UserError(f"HTTP error {e.code}: {e.reason}")
        except Exception as e:
            raise UserError(f"Request failed: {e}")

        # Build top_values string for text/string fields
        def fmt_top(values):
            if not values:
                return ''
            return ', '.join(f"{v['value']}({v['count']})" for v in values)

        inv = self.env['inventory.imported_inventory'].create({
            'name': data.get('title', ''),
            'description': data.get('description', ''),
            'item_count': data.get('itemCount', 0),
        })

        for f in data.get('fields', []):
            self.env['inventory.imported_field'].create({
                'inventory_id': inv.id,
                'name': f.get('name', ''),
                'field_type': f.get('type', ''),
                'slot': f.get('slot', ''),
                'total_items': f.get('totalItems', 0),
                'filled_count': f.get('filledCount', 0),
                'fill_percent': f.get('fillPercent', 0),
                'num_min': f.get('numMin') or 0.0,
                'num_max': f.get('numMax') or 0.0,
                'num_avg': f.get('numAvg') or 0.0,
                'bool_true_count': f.get('boolTrueCount', 0),
                'bool_false_count': f.get('boolFalseCount', 0),
                'bool_null_count': f.get('boolNullCount', 0),
                'top_values': fmt_top(f.get('topValues', [])),
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'inventory.imported_inventory',
            'res_id': inv.id,
            'view_mode': 'form',
            'target': 'current',
        }
