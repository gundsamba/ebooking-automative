from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Product(models.Model):
  _inherit = 'product.category'
  _rec_name = 'name'

  @api.model
  def create(self, vals):
    if self.env.context.get('is_repair', False):
      vals.update({'parent_id': self.env.ref('ebooking_auto.product_category_repair').id})
    if self.env.context.get('is_part', False):
      vals.update({'parent_id': self.env.ref('ebooking_auto.product_category_part').id})
    return super(Product, self).create(vals)

class ProductTemplate(models.Model):
  _inherit = 'product.template'

  @api.model
  def create(self, vals):
    if self.env.context.get('is_diagnostic', False):
      vals.update({'categ_id': self.env.ref('ebooking_auto.product_category_diagnostic').id})
    return super(ProductTemplate, self).create(vals)
