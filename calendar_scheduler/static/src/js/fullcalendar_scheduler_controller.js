odoo.define('fullcalendar.scheduler_controller', function (require) {
    "use strict";

    var CalendarController = require('web.CalendarController');
    var core = require('web.core');
    var QWeb = core.qweb;

    CalendarController.include({
        renderButtons: function ($node) {
            var self = this;
            this.$buttons = $(QWeb.render("CalendarView.buttons", {'widget': this}));
            this.$buttons.on('click', 'button.o_calendar_button_new', function () {
                self.trigger_up('switch_view', {view_type: 'form'});
            });

            _.each(['prev', 'today', 'next'], function (action) {
                self.$buttons.on('click', '.o_calendar_button_' + action, function () {
                    self.model[action]();
                    self.reload();
                });
            });
            _.each(['day', 'week', 'month', 'timeline'], function (scale) {
                self.$buttons.on('click', '.o_calendar_button_' + scale, function () {
                    self.model.setScale(scale);
                    self.reload();
                });
            });

            this.$buttons.find('.o_calendar_button_' + this.mode).addClass('active');

            if ($node) {
                this.$buttons.appendTo($node);
            } else {
                this.$('.o_calendar_buttons').replaceWith(this.$buttons);
            }
        },
        _onChangeDate: function (event) {
            var modelData = this.model.get();
            if (modelData.target_date.format('YYYY-MM-DD') === event.data.date.format('YYYY-MM-DD')) {
                // When clicking on same date, toggle between the two views
                switch (modelData.scale) {
                    case 'month': this.model.setScale('week'); break;
                    case 'week': this.model.setScale('day'); break;
                    case 'day': this.model.setScale('month'); break;
                    case 'timeline': this.model.setScale('timeline'); break;
                }
            } else if (modelData.target_date.week() === event.data.date.week()) {
                // When clicking on a date in the same week, switch to day view
                this.model.setScale('day');
            } else {
                // When clicking on a random day of a random other week, switch to week view
                this.model.setScale('week');
            }
            this.model.setDate(event.data.date);
            this.reload();
        },
    });
});
