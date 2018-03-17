# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Vehicle(models.Model):
  _inherit = 'fleet.vehicle'

  customer_company_type = fields.Selection(string='Company Type', selection=[('person', 'Хувь хүн'), ('company', 'Байгууллага')],
        compute='_compute_company_type', inverse='_write_company_type')
  customer_is_company = fields.Boolean(string='Is a Company', default=False, help="Check if the contact is a company, otherwise it is a person")
  customer_name = fields.Char()
  customer_phone = fields.Char()
  customer_mobile = fields.Char()
  customer_contact_address = fields.Char(string='Complete Address')

  @api.depends('customer_is_company')
  def _compute_company_type(self):
      for partner in self:
          partner.customer_company_type = 'company' if partner.customer_is_company else 'person'

  def _write_company_type(self):
      for partner in self:
          partner.customer_is_company = partner.customer_company_type == 'company'
