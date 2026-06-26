{
    'name': 'Stock Threshold Dashboard',
    'version': '1.0',
    'summary': 'A visual dashboard for monitoring critical inventory levels with OWL',
    'category': 'Inventory/Inventory',
    'author': 'Hezkiel Chris T',
    'depends': ['stock', 'web'],
    'data': [
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_stock_dashboard/static/src/js/stock_dashboard.js',
            'custom_stock_dashboard/static/src/xml/stock_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}