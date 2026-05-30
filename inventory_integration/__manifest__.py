{
    'name': 'Inventory Integration',
    'version': '1.0.0',
    'summary': 'Import aggregated inventory data from the external Inventory Management app',
    'description': """
        Connects to the Inventory Management web application via an API token and imports:
        - Inventory title and item count
        - Field definitions (name + type)
        - Aggregated statistics per field (min/max/avg for numbers,
          top values for text/string, true/false counts for booleans)

        The module is read-only: data flows from the external app into Odoo.
    """,
    'category': 'Inventory',
    'author': 'Inventory Management Integration',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/imported_inventory_views.xml',
        'views/imported_field_views.xml',
        'views/menu.xml',
        'wizard/import_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
