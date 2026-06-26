from odoo import models, fields, api

class QcChecklist(models.Model):
    _name = 'qc.checklist'
    _description = 'Quality Control Checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    picking_id = fields.Many2one(
        'stock.picking', 
        string='Receipt Transfer', 
        required=True, 
        domain="[('picking_type_id.code', '=', 'incoming'), ('state', '=', 'done')]"
    )
    
    check_date = fields.Datetime(string='Check Date', default=fields.Datetime.now, required=True)
    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda self: self.env.user)
    is_quantity_match = fields.Boolean(string='Quantity Matches PO?', tracking=True)
    is_packaging_good = fields.Boolean(string='Packaging in Good Condition?', tracking=True)
    
    is_passed = fields.Boolean(
        string='Passed Quality Control', 
        compute='_compute_is_passed',
        inverse='_inverse_is_passed',
        store=True,
        tracking=True
    )
    notes = fields.Text(string='Inspection Notes')

    @api.depends('is_quantity_match', 'is_packaging_good')
    def _compute_is_passed(self):
        for record in self:
            record.is_passed = record.is_quantity_match and record.is_packaging_good

    def _inverse_is_passed(self):
        for record in self:
            record.is_quantity_match = record.is_passed
            record.is_packaging_good = record.is_passed
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Completed')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qc.checklist.seq') or 'New'
        return super().create(vals_list)

    def action_confirm_qc(self):
        for record in self:
            record.state = 'done'
            record._mark_picking_activity_done()

    def _mark_picking_activity_done(self):
        activity_type_todo = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type_todo:
            return
            
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'stock.picking'),
            ('res_id', '=', self.picking_id.id),
            ('activity_type_id', '=', activity_type_todo.id),
            ('summary', 'ilike', 'Pending QC Checklist')
        ])
        if activities:
            activities.action_done()