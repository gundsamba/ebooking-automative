# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
  _inherit = 'hr.employee'

  first_name = fields.Char()
  last_name = fields.Char()
  middle_name = fields.Char()

  @api.onchange('first_name','last_name')
  def _onchange_first_last_name(self):
    self.name = '%s %s' % (self.last_name, self.first_name)
