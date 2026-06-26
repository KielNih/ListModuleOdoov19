from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.document'
    _description = 'HR Employee Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Document Name', required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    expiry_date = fields.Date(string='Expiry Date', required=True, tracking=True)
    is_expiry_notified = fields.Boolean(string='Is Expiry Notified', default=False, copy=False)

    # Tambahkan 2 Computed Field ini
    is_expired = fields.Boolean(string='Is Expired', compute='_compute_document_status')
    is_expiring_soon = fields.Boolean(string='Is Expiring Soon', compute='_compute_document_status')

    @api.depends('expiry_date')
    def _compute_document_status(self):
        """
        Kalkulasi status dokumen secara real-time di backend.
        Tidak disimpan di database (tanpa store=True) agar selalu akurat setiap hari.
        """
        today = fields.Date.today()
        limit_date = today + relativedelta(days=30)
        
        for doc in self:
            if doc.expiry_date:
                doc.is_expired = doc.expiry_date < today
                # True jika tanggal hari ini berada dalam rentang 30 hari sebelum expired
                doc.is_expiring_soon = today <= doc.expiry_date <= limit_date
            else:
                doc.is_expired = False
                doc.is_expiring_soon = False

    def write(self, vals):
        if 'expiry_date' in vals:
            vals['is_expiry_notified'] = False
        return super(HrEmployeeDocument, self).write(vals)

    @api.model
    def _cron_check_document_expiry(self):
        limit_date = fields.Date.today() + relativedelta(days=30)
        documents = self.search([
            ('expiry_date', '<=', limit_date),
            ('is_expiry_notified', '=', False)
        ])
        
        for doc in documents:
            assignee_id = doc.employee_id.parent_id.user_id.id or doc.create_uid.id
            if assignee_id:
                doc.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=f'Document Expiring Soon: {doc.name}',
                    note=f'The document {doc.name} for {doc.employee_id.name} will expire on {doc.expiry_date}. Please take action for renewal.',
                    user_id=assignee_id,
                    date_deadline=doc.expiry_date
                )
                doc.is_expiry_notified = True