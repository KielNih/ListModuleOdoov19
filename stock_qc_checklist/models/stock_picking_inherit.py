from odoo import models, fields, api
from datetime import datetime, time

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    qc_checklist_ids = fields.One2many('qc.checklist', 'picking_id', string='QC Checklists')
    qc_checklist_count = fields.Integer(string='QC Checklist Count', compute='_compute_qc_checklist_count')

    @api.depends('qc_checklist_ids')
    def _compute_qc_checklist_count(self):
        for picking in self:
            picking.qc_checklist_count = len(picking.qc_checklist_ids)

    def _action_done(self):
        res = super(StockPicking, self)._action_done()

        for picking in self:
            if picking.picking_type_id.code == 'incoming' and not picking.qc_checklist_ids:
                self.env['qc.checklist'].create({
                    'picking_id': picking.id,
                })
        return res

    @api.model
    def _cron_check_missing_qc(self):
        today_start = datetime.combine(fields.Date.today(), time.min)
        today_end = datetime.combine(fields.Date.today(), time.max)
        missing_qc_pickings = self.search([
            ('picking_type_id.code', '=', 'incoming'),
            ('state', '=', 'done'),
            ('date_done', '>=', today_start),
            ('date_done', '<=', today_end),
            ('qc_checklist_ids.state', '=', 'draft') 
        ])

        for picking in missing_qc_pickings:
            existing_activity = self.env['mail.activity'].search([
                ('res_id', '=', picking.id),
                ('res_model', '=', 'stock.picking'),
                ('summary', '=', 'Pending QC Checklist')
            ], limit=1)

            if not existing_activity:
                assignee_id = picking.user_id.id or picking.write_uid.id or self.env.ref('base.user_admin').id
                
                # Membuat To-Do activity
                picking.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=assignee_id,
                    summary='Pending QC Checklist',
                    note=f'Please complete the Quality Control checklist for receipt {picking.name} before the end of the day.'
                )