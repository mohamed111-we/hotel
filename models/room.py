from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room Details'

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    name = fields.Char(string='Room Name', required=True, default='Room >> ')
    room_number = fields.Char(string='Room Number', required=True)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite')],
        string='Room Type', required=True)
    floor_number = fields.Integer(string='Floor Number', required=True)
    night_price = fields.Float(string='Night Price', required=True)
    state = fields.Selection([
        ('empty', 'Empty'),
        ('busy', 'Busy'),
        ('maintenance', 'Maintenance'),
    ], string='State', default='empty')
    reservation_ids = fields.One2many('room.reservation','room_id', string='Room Reservation')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('room.room') or _('New')
        return super(Room, self).create(vals_list)

    @api.constrains('night_price', 'floor_number')
    def _check_night_price(self):
        for record in self:
            if record.night_price <= 0:
                raise ValidationError(_("The 'Night Price' field must be a positive value."))
            if record.floor_number <= 0:
                raise ValidationError(_("The 'Floor Number' field must be a positive value."))

    def action_empty(self):
        for rec in self:
            rec.state = 'empty'


    def action_maintenance(self):
        for rec in self:
            rec.state = 'maintenance'