{
    'name': 'Inventory Integration',
    'version': '1.0',
    'summary': 'Import inventory data from external API',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
        'views/imported_inventory_views.xml',
    ],
    'installable': True,
    'application': True,
}
