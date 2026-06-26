{
    'name': 'Auto QC Checklist for Goods Received',
    'version': '1.0',
    'summary': 'Automated Quality Control checklist and activity reminder for incoming shipments.',
    'category': 'Inventory/Inventory',
    'author': 'Hezkiel Chris T',
    'depends': ['stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_job.xml',
        'views/qc_checklist_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}