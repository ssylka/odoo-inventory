import json
import urllib.request
import urllib.error
from datetime import datetime

from odoo import models, fields, _
from odoo.exceptions import UserError


class ImportWizard(models.TransientModel):
    """
    Wizard that fetches data from the Inventory Management API and writes it
    into ``inventory.integration.imported_inventory`` + child field records.

    Two usage modes:
    - "New import": user fills in api_url + api_token, no inventory_id set.
      A new ImportedInventory record is created.
    - "Re-import": opened from an existing record (inventory_id is pre-set).
      The existing record (and its fields) is refreshed in-place.
    """
    _name = 'inventory.integration.import_wizard'
    _description = 'Import Inventory Wizard'

    api_url = fields.Char(
        string='API Base URL',
        required=True,
        help='E.g. https://my-app.onrender.com  (no trailing slash)',
    )
    api_token = fields.Char(
        string='API Token',
        required=True,
        help='Token generated in the Inventory Management app (API Token tab).',
    )
    inventory_id = fields.Many2one(
        comodel_name='inventory.integration.imported_inventory',
        string='Update existing record',
        help='Leave empty to create a new record.',
    )

    # ── Main action ───────────────────────────────────────────────────────────

    def action_import(self):
        self.ensure_one()

        data = self._fetch_api()

        inv_model = self.env['inventory.integration.imported_inventory']
        fld_model = self.env['inventory.integration.imported_field']

        # Determine whether to create or update
        inventory = self.inventory_id
        if not inventory:
            inventory = inv_model.create({
                'name':        data['title'],
                'external_id': data['inventoryId'],
                'description': data.get('description', ''),
                'api_url':     self.api_url,
                'api_token':   self.api_token,
            })
        else:
            inventory.write({
                'name':        data['title'],
                'external_id': data['inventoryId'],
                'description': data.get('description', ''),
            })
            # Delete stale field rows so we rebuild them cleanly
            fld_model.search([('inventory_id', '=', inventory.id)]).unlink()

        # Write fields + stats
        for f in data.get('fields', []):
            top_values_json = json.dumps(
                [{'value': tv['value'], 'count': tv['count']} for tv in f.get('topValues', [])],
                ensure_ascii=False,
            )
            fld_model.create({
                'inventory_id':    inventory.id,
                'name':            f.get('name', ''),
                'field_type':      f.get('type', ''),
                'slot':            f.get('slot', ''),
                'total_items':     f.get('totalItems', 0),
                'filled_count':    f.get('filledCount', 0),
                'fill_percent':    f.get('fillPercent', 0),
                'num_min':         f.get('numMin') or 0.0,
                'num_max':         f.get('numMax') or 0.0,
                'num_avg':         f.get('numAvg') or 0.0,
                'top_values':      top_values_json,
                'bool_true_count':  f.get('boolTrueCount', 0),
                'bool_false_count': f.get('boolFalseCount', 0),
                'bool_null_count':  f.get('boolNullCount', 0),
            })

        inventory.write({
            'item_count':    data.get('itemCount', 0),
            'last_imported': fields.Datetime.now(),
        })

        # Open the imported inventory form
        return {
            'type': 'ir.actions.act_window',
            'name': _('Imported Inventory'),
            'res_model': 'inventory.integration.imported_inventory',
            'res_id': inventory.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ── HTTP helper ───────────────────────────────────────────────────────────

    def _fetch_api(self):
        """
        Call GET <api_url>/api/inventory?token=<api_token> and return the
        parsed JSON dict.  Raises UserError on any network or HTTP problem.
        """
        base = self.api_url.rstrip('/')
        url  = f'{base}/api/inventory?token={self.api_token}'

        try:
            req = urllib.request.Request(
                url,
                headers={'Accept': 'application/json'},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            raise UserError(
                _('HTTP %(code)s from %(url)s:\n%(body)s',
                  code=e.code, url=url, body=body)
            )
        except urllib.error.URLError as e:
            raise UserError(
                _('Cannot reach %(url)s:\n%(reason)s', url=url, reason=str(e.reason))
            )

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise UserError(
                _('Invalid JSON returned by the API:\n%(err)s', err=str(e))
            )
