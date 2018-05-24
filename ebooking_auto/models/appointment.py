# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)

class Appointment(models.Model):
  _name = 'ebooking_auto.appointment'

  company_id = fields.Many2one('res.company', string = "Company", change_default=True, required=True, readonly=True,
    default=lambda self: self.env['res.company']._company_default_get('ebooking_auto.appointment'))
  resource_id = fields.Many2one('ebooking_auto.resource', string = "Өргөгч")
  # customer_id = fields.Many2one('res.partner', string = "Customer")
  begin_date = fields.Datetime(string = "Begin date")
  end_date = fields.Datetime(string = "End date")
  appointment_type = fields.Selection(string = "Захиалгын төрөл", selection = [
    (1, "Биечлэн"),
    (2, "Утсаар")
  ])
  state = fields.Selection(string = "Захиалгын төлөв", selection = [
    ('order', "Захиалганд байгаа"),
    ('wait', "Хүлээлгэнд байгаа"),
    ('serve', "Үйлчилгээнд орсон"),
    ('complete', "Үйлчлүүлж дууссан"),
    ('paid', "Төлбөр төлөгдсөн"),
    ('cancel', "Цуцалсан")
  ], default='order', readonly=True)
  state_color = fields.Char(compute='_compute_state_color', store=True)
  cancel_memo = fields.Text(string = "Цуцлагдсан тайлбар")
  request_type_ids = fields.Many2many('ebooking_auto.request_type', string = "Үйлчлүүлэгчийн хүсэлтийн төрөл")
  request_memo = fields.Text(string = "Үйлчлүүлэгчийн хүсэлт")
  vehicle_id = fields.Many2one('fleet.vehicle', string = "Vehicle", required=True)
  vehicle_license_plate = fields.Char(related='vehicle_id.license_plate', help='License plate number of the vehicle (i = plate number for a car)')
  vehicle_model_id = fields.Many2one('fleet.vehicle.model', 'Model', help='Model of the vehicle', readonly=True, related='vehicle_id.model_id')
  vehicle_model_year = fields.Char('Model Year',help='Year of the model', readonly=True, related='vehicle_id.model_year')
  vehicle_vin_sn = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)', copy=False, readonly=True, related='vehicle_id.vin_sn')
  vehicle_fuel_type = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
        ], 'Fuel Type', help='Fuel Used by the vehicle', readonly=True, related='vehicle_id.fuel_type')
  vehicle_transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle', readonly=True, related='vehicle_id.transmission')
  vehicle_odometer = fields.Float(string='Last Odometer', readonly=True, related='vehicle_id.odometer')
  vehicle_odometer_unit = fields.Selection([
      ('kilometers', 'Kilometers'),
      ('miles', 'Miles')
      ], 'Odometer Unit', default='kilometers', help='Unit of the odometer ', readonly=True, related='vehicle_id.odometer_unit')
  vehicle_isownsold = fields.Boolean(string='Манайхаас худалдан авсан эсэх', readonly=True, related='vehicle_id.vehicle_isownsold')
  customer_name = fields.Char(string='Эзэмшигчийн нэр', related='vehicle_id.customer_name')
  customer_phone = fields.Char(string='Утас', related='vehicle_id.customer_phone')
  customer_mobile = fields.Char(string='Гар утас', related='vehicle_id.customer_mobile')
  customer_is_company = fields.Boolean(string='Is a Company', default=False,
        help="Check if the contact is a company, otherwise it is a person", related='vehicle_id.customer_is_company')
  customer_company_type = fields.Selection(string='Эзэмшигч',
        selection=[('person', 'Хувь хүн'), ('company', 'Байгууллага')], readonly=True, related='vehicle_id.customer_company_type')
  customer_contact_address = fields.Char(string='Хаяг', readonly=True, related='vehicle_id.customer_contact_address')
  customer_email = fields.Char(string='И-мэйл', readonly=True, related='vehicle_id.customer_email')

  @api.onchange('vehicle_id')
  def _onchange_vehicle_id(self):
    self.vehicle_license_plate = self.vehicle_id.license_plate
    self.vehicle_model_id = self.vehicle_id.model_id
    self.vehicle_model_year = self.vehicle_id.model_year
    self.vehicle_vin_sn = self.vehicle_id.vin_sn
    self.vehicle_fuel_type = self.vehicle_id.fuel_type
    self.vehicle_transmission = self.vehicle_id.transmission
    self.vehicle_odometer = self.vehicle_id.odometer
    self.vehicle_odometer_unit = self.vehicle_id.odometer_unit
    self.vehicle_isownsold = self.vehicle_id.vehicle_isownsold
    self.customer_name = self.vehicle_id.customer_name
    self.customer_phone = self.vehicle_id.customer_phone
    self.customer_mobile = self.vehicle_id.customer_mobile
    self.customer_is_company = self.vehicle_id.customer_is_company
    self.customer_company_type = self.vehicle_id.customer_company_type
    self.customer_contact_address = self.vehicle_id.customer_contact_address
    self.customer_email = self.vehicle_id.customer_email

  @api.depends('state')
  def _compute_state_color(self):
    # if self.state == 'order':
    #   self.state_color = '#4c4f53'
    # elif self.state == 'wait':
    #   self.state_color = '#ac5287'
    # elif self.state == 'serve':
    #   self.state_color = '#c79121'
    # elif self.state == 'complete':
    #   self.state_color = '#57889c'
    # elif self.state == 'paid':
    #   self.state_color = '#71843f'
    # elif self.state == 'cancel':
    #   self.state_color = '#a90329'
    if self.state == 'order':
      self.state_color = '#4c4f53'
    elif self.state == 'wait':
      self.state_color = '#ac5287'
    elif self.state == 'serve':
      self.state_color = '#f0ad4e'
    elif self.state == 'complete':
      self.state_color = '#337ab7'
    elif self.state == 'paid':
      self.state_color = '#5cb85c'
    elif self.state == 'cancel':
      self.state_color = '#d9534f'

  diagnostic_type_ids = fields.Many2many('product.template', string = "Оношлогооны төрөл")
  diagnostic_desc = fields.Text(string = "Оношлогооны дүгнэлт")
  diagnostic_seniormechanical_id = fields.Many2one('res.users', string = "Дүгнэлт гаргасан ахлах механик")
  diagnostic_mechanical_id = fields.Many2one('res.users', string = "Дүгнэлт гаргасан механик")
  diagnostic_serviceconsultant_id = fields.Many2one('res.users', string = "Дүгнэлт гаргасан үйлчилгээний зөвлөх")

  repair_type_ids = fields.Many2many('ebooking_auto.repair_type', string = "ЗҮ орох төрөл")
  repair_line_ids = fields.One2many('ebooking_auto.repair.line', 'appointment_id', string='Repair Lines', copy=True)
  repair_seniormechanical_id = fields.Many2one('res.users', string = "Засварласан ахлах механик")
  repair_mechanical_id = fields.Many2one('res.users', string = "Засварласан механик")
  repair_serviceconsultant_id = fields.Many2one('res.users', string = "Шалгасан үйлчилгээний зөвлөх")
  repair_desc = fields.Text(string = "Засварын үр дүн")

  part_line_ids = fields.One2many('ebooking_auto.part.line', 'appointment_id', string='Part Lines', copy=True)

  @api.multi
  def action_appointment_wait(self):
    self.write({'state': 'wait'})

  @api.multi
  def action_appointment_serve(self):
    self.write({'state': 'serve'})

  @api.multi
  def action_appointment_complete(self):
    self.write({'state': 'complete'})

  @api.multi
  def action_appointment_paid(self):
    self.write({'state': 'paid'})

  @api.multi
  def action_appointment_cancel(self):
    self.write({'state': 'cancel'})

class Resource(models.Model):
  _name = 'ebooking_auto.resource'

  company_id = fields.Many2one('res.company', string='Company', change_default=True, required=True, readonly=True,
    default=lambda self: self.env.user.company_id.id)
  num = fields.Integer(string='Өргөгчийн дугаар', required=True)
  desc = fields.Char(string='Өргөгчийн нэр')
  name = fields.Char(string='Өргөгч', compute='_compute_name')
  is_active = fields.Boolean(compute='_compute_is_active')

  @api.one
  def _compute_is_active(self):
    capacity = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.resource_capacity', default='1')
    if int(self.num) <= int(capacity):
      self.is_active = True
    else:
      self.is_active = False

  @api.one
  @api.depends('num', 'desc')
  def _compute_name(self):
    names = [str(self.num), self.desc]
    self.name = ' '.join(filter(None, names))

  @api.model
  def search(self, args, offset=0, limit=None, order=None, count=False):
    capacity = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.resource_capacity', default='1')
    args += [('num', '<=', int(capacity))]
    return super(Resource, self).search(args, offset, limit, order, count=count)

  @api.model
  def resource_list(self):
    capacity = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.resource_capacity', default='1')
    timeline_starttime = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.timeline_starttime', default='00:00')
    timeline_endtime = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.timeline_endtime', default='23:30')
    timeline_interval = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.timeline_interval', default='15')
    timeline_lunchstarttime = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.timeline_interval', default='00:00')
    timeline_lunchendtime = self.env['ir.config_parameter'].sudo().get_param('ebooking_auto.timeline_lunchendtime', default='23:30')
    domain = []
    domain = expression.AND([domain, [('num', '<=', capacity)]])
    res_data = (
      self.search(domain).read(['company_id', 'num', 'name']),
      timeline_starttime,
      timeline_endtime,
      timeline_interval,
      timeline_lunchstarttime,
      timeline_lunchendtime
      )
    return res_data

# class ConfigParameter(models.Model):
#   _inherit = 'ir.config_parameter'

#   @api.model
#   def search(self, args, offset=0, limit=None, order=None, count=False):
#     context = self._context or {}
#     if context.get('is_resource_capacity'):
#       args += [('key', '=', 'ebooking_auto.resource_capacity')]
#     return super(ConfigParameter, self).search(args, offset, limit, order, count=count)

#   @api.multi
#   def unlink(self):
#     config_list = self.env['ir.config_parameter'].search([('id', 'in', self.ids)])
#     for config in config_list:
#       if str(config.key) == 'ebooking_auto.resource_capacity':
#         raise UserError(_('Өргөгчийн тооны тохиргоог устгах боломжгүй.'))
#     return super(ConfigParameter, self).unlink()

class RequestType(models.Model):
  _name = 'ebooking_auto.request_type'

  name = fields.Char(string = "Нэр")

class RepairType(models.Model):
  _name = 'ebooking_auto.repair_type'

  name = fields.Char(string = "Нэр")

class AppointmentRepairLine(models.Model):
  _name = "ebooking_auto.repair.line"

  @api.one
  @api.depends('price_unit', 'discount', 'quantity', 'product_id')
  def _compute_price(self):
    currency = self.company_currency_id
    price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
    taxes = False
    if self.tax_ids:
        taxes = self.tax_ids.compute_all(price, currency, self.quantity, product=self.product_id)
    self.price_subtotal = taxes['total_excluded'] if taxes else self.quantity * price
    self.price_total = taxes['total_included'] if taxes else self.price_subtotal

  appointment_id = fields.Many2one('ebooking_auto.appointment', string = "Засварын захиалга", required=True)
  product_id = fields.Many2one('product.product', string='Засвар үйлчилгээ', required=True)
  name = fields.Text(string='Тайлбар', required=True)
  price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'))
  price_subtotal = fields.Monetary(string='Amount',currency_field='company_currency_id', store=True, readonly=True, compute='_compute_price', help="Total amount without taxes")
  price_total = fields.Monetary(string='Amount',currency_field='company_currency_id', store=True, readonly=True, compute='_compute_price', help="Total amount with taxes")
  tax_ids = fields.Many2many('account.tax', string='Татвар', domain=['|', ('active', '=', False), ('active', '=', True)])
  quantity = fields.Float(string='Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'), required=True)
  discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'),default=0.0)
  company_currency_id = fields.Many2one('res.currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id)
#     product_category_name = fields.Char()
#     product_code = fields.Char()
#     product_name = fields.Char()
#     product_desc = fields.Char()

class AppointmentPartLine(models.Model):
  _name = "ebooking_auto.part.line"

  @api.one
  @api.depends('price_unit', 'discount', 'quantity', 'product_id')
  def _compute_price(self):
    currency = self.company_currency_id
    price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
    taxes = False
    if self.tax_ids:
        taxes = self.tax_ids.compute_all(price, currency, self.quantity, product=self.product_id)
    self.price_subtotal = taxes['total_excluded'] if taxes else self.quantity * price
    self.price_total = taxes['total_included'] if taxes else self.price_subtotal

  appointment_id = fields.Many2one('ebooking_auto.appointment', string = "Засварын захиалга", required=True)
  product_id = fields.Many2one('product.product', string='Сэлбэг', required=True)
  name = fields.Text(string='Тайлбар', required=True)
  price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'))
  price_subtotal = fields.Monetary(string='Amount',currency_field='company_currency_id', store=True, readonly=True, compute='_compute_price', help="Total amount without taxes")
  price_total = fields.Monetary(string='Amount',currency_field='company_currency_id', store=True, readonly=True, compute='_compute_price', help="Total amount with taxes")
  tax_ids = fields.Many2many('account.tax', string='Татвар', domain=['|', ('active', '=', False), ('active', '=', True)])
  quantity = fields.Float(string='Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'), required=True)
  discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'),default=0.0)
  company_currency_id = fields.Many2one('res.currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id)
#     product_category_name = fields.Char()
#     product_code = fields.Char()
#     product_name = fields.Char()
#     product_desc = fields.Char()
