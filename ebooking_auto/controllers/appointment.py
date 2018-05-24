# -*- coding: utf-8 -*-

from odoo import http

class Appointment(http.Controller):

    @http.route('/app/app/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('ebooking_auto.index', {})
