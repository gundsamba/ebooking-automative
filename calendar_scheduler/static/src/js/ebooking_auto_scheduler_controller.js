odoo.define('calendar_scheduler.scheduler_controller', function (require) {
    "use strict";

    var CalendarController = require('web.CalendarController');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    CalendarController.include({
        _onOpenCreate: function (event) {
            var self = this;
            if (this.model.get().scale === "month") {
                event.data.allDay = true;
            }
            var data = this.model.calendarEventToRecord(event.data);

            var context = _.extend({}, this.context, event.options && event.options.context);
            context.default_name = data.name || null;
            context['default_' + this.mapping.date_start] = data[this.mapping.date_start] || null;
            if (this.mapping.date_stop) {
                context['default_' + this.mapping.date_stop] = data[this.mapping.date_stop] || null;
            }
            if (this.mapping.date_delay) {
                context['default_' + this.mapping.date_delay] = data[this.mapping.date_delay] || null;
            }
            if (this.mapping.all_day) {
                context['default_' + this.mapping.all_day] = data[this.mapping.all_day] || null;
            }
            if (this.model.get().scale === "timeline") {
                context['default_resource_id'] = (parseInt($('.fc-highlight').closest('tr').index()) + 1) || null;
            }

            for (var k in context) {
                if (context[k] && context[k]._isAMomentObject) {
                    context[k] = context[k].clone().utc().format('YYYY-MM-DD HH:mm:ss');
                }
            }

            var options = _.extend({}, this.options, event.options, {context: context});

            if (this.quick != null) {
                this.quick.destroy();
                this.quick = null;
            }

            var title = _t("Create");
            if (this.renderer.arch.attrs.string) {
                title += ': ' + this.renderer.arch.attrs.string;
            }
            if (!this.eventOpenPopup) {
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: this.modelName,
                    views: [[this.formViewId || false, 'form']],
                    target: 'current',
                    context: context,
                });
            }
        },
    });
});
