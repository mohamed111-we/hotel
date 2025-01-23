from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RoomReservation(models.Model):
    _name = 'room.reservation'
    _description = 'Room Reservation Details'

    name = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    customer_id = fields.Many2one('res.partner', 'Customer', tracking=True)
    phone = fields.Char(related='customer_id.phone', string="Phone Number", store=True, readonly=True)
    email = fields.Char(related="customer_id.email", string="Email", store=True, readonly=True)
    address = fields.Char(related="customer_id.street", string="Address", store=True, readonly=True)
    id_type = fields.Selection([
        ('passport', 'Passport'),
        ('national_id', 'National ID'),
        ('driving_license', 'Driving License'),
    ], string="ID Type", help="Select the type of ID.")
    id_number = fields.Char(string="ID Number", help="Enter the ID number.")
    start_date = fields.Date(string="Start Date", help="Start date of the reservation.")
    end_date = fields.Date(string="End Date", help="End date of the reservation.")
    duration = fields.Integer(string="Duration (Days)", compute='_compute_duration',
                              help="Duration of the reservation in days.")
    note = fields.Text('Internal Notes', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('ending', 'Ending'),
    ], string="State", default="draft")
    reservation_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite')],
        string='Room Type', required=True)
    room_id = fields.Many2one('room.room', string="Room", required=True)

    @api.constrains('start_date', 'end_date', 'room_id')
    def _check_room_availability(self):
        for rec in self:
            overlapping_reservations = self.env['room.reservation'].search([
                ('room_id', '=', rec.room_id.id),
                ('start_date', '<=', rec.end_date),
                ('end_date', '>=', rec.start_date),
                ('id', '!=', rec.id),
            ])
            if overlapping_reservations:
                reservation_dates = ""
                for res in overlapping_reservations:
                    reservation_dates += f"From {res.start_date} to {res.end_date} (Reference: {res.name})\n"
                raise ValidationError(
                    _("The room is already reserved for the selected dates. Please choose different dates.\n\n"
                      "Conflicting reservations:\n" + reservation_dates))


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('room.reservation') or _('New')
        return super(RoomReservation, self).create(vals_list)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration = max((rec.end_date - rec.start_date).days, 0)
            else:
                rec.duration = 0

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_scheduled(self):
        for rec in self:
            rec.state = 'scheduled'

    def action_running(self):
        for rec in self:
            rec.state = 'running'

    def action_ending(self):
        for rec in self:
            rec.state = 'ending'
