{
    'name': 'HR Document Expiry Tracker',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Proactively track employee document expiry dates and notify HR.',
    'description': """
        This module allows HR to track employee documents (ID Card, Driver's License, Contracts)
        and automatically creates an Activity 30 days before the document expires.
    """,
    'author': 'Hezkiel Chris T',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/hr_employee_document_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}