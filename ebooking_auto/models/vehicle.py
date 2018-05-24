# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Vehicle(models.Model):
  _inherit = 'fleet.vehicle'

  vehicle_isownsold = fields.Boolean(string='Манайхаас худалдан авсан эсэх')
  customer_name = fields.Char(string='Эзэмшигчийн нэр')
  customer_phone = fields.Char(string='Утас')
  customer_mobile = fields.Char(string='Гар утас')
  customer_is_company = fields.Boolean(string='Is a Company', default=False,
        help="Check if the contact is a company, otherwise it is a person")
  customer_company_type = fields.Selection(string='Эзэмшигч',
        selection=[('person', 'Хувь хүн'), ('company', 'Байгууллага')],
        compute='_compute_company_type', inverse='_write_company_type')
  customer_contact_address = fields.Char(string='Хаяг')
  customer_email = fields.Char(string='И-мэйл')

  @api.depends('customer_is_company')
  def _compute_company_type(self):
    for partner in self:
      partner.customer_company_type = 'company' if partner.customer_is_company else 'person'

  def _write_company_type(self):
    for partner in self:
      partner.customer_is_company = partner.customer_company_type == 'company'

  @api.onchange('customer_company_type')
  def onchange_customer_company_type(self):
    self.customer_is_company = (self.customer_company_type == 'company')
