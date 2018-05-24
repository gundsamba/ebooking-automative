odoo.define('fullcalendar.scheduler_view', function (require) {
    "use strict";

    var CalendarView = require('web.CalendarView');
    var core = require('web.core');
    var QWeb = core.qweb;

    CalendarView.include({
        jsLibs: ['/web/static/lib/fullcalendar/js/fullcalendar.js', '/calendar_scheduler/static/lib/fullcalendar/js/scheduler.min.js'],
        cssLibs: ['/web/static/lib/fullcalendar/css/fullcalendar.css', '/calendar_scheduler/static/lib/fullcalendar/css/scheduler.min.css'],
    });
});
