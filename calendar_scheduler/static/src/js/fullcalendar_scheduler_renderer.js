odoo.define('fullcalendar.scheduler_renderer', function (require) {
    "use strict";

    var CalendarRenderer = require('web.CalendarRenderer');

    var scales = {
        timeline: 'timelineDay',
        day: 'agendaDay',
        week: 'agendaWeek',
        month: 'month'
    };

    CalendarRenderer.include({
        _initCalendar: function () {
            var self = this;

            this.$calendar = this.$(".o_calendar_widget");

            //Documentation here : http://arshaw.com/fullcalendar/docs/
            var fc_options = $.extend({}, this.state.fc_options, {
                eventDrop: function (event) {
                    self.trigger_up('dropRecord', event);
                },
                eventResize: function (event) {
                    self.trigger_up('updateRecord', event);
                },
                eventClick: function (event) {
                    self.trigger_up('openEvent', event);
                    self.$calendar.fullCalendar('unselect');
                },
                select: function (target_date, end_date, event, _js_event, _view) {
                    var data = {'start': target_date, 'end': end_date};
                    if (self.state.context.default_name) {
                        data.title = self.state.context.default_name;
                    }
                    self.trigger_up('openCreate', data);
                    self.$calendar.fullCalendar('unselect');
                },
                eventRender: function (event, element) {
                    var $render = $(self._eventRender(event));
                    event.title = $render.find('.o_field_type_char:first').text();
                    element.find('.fc-content').html($render.html());
                    element.addClass($render.attr('class'));
                    var display_hour = '';
                    if (!event.allDay) {
                        var start = event.r_start || event.start;
                        var end = event.r_end || event.end;
                        display_hour = start.format('HH:mm') + ' - ' + end.format('HH:mm');
                        if (display_hour === '00:00 - 00:00') {
                            display_hour = _t('All day');
                        }
                    }
                    element.find('.fc-content .fc-time').text(display_hour);
                },
                // Dirty hack to ensure a correct first render
                eventAfterAllRender: function () {
                    $(window).trigger('resize');
                },
                viewRender: function (view) {
                    // compute mode from view.name which is either 'month', 'agendaWeek' or 'agendaDay'
                    var mode = view.name === 'month' ? 'month' : (view.name === 'agendaWeek' ? 'week' : (view.name === 'agendaDay' ? 'day' : 'timeline'));
                    // compute title: in week mode, display the week number
                    var title = mode === 'week' ? view.intervalStart.week() : view.title;
                    self.trigger_up('viewUpdated', {
                        mode: mode,
                        title: title,
                    });
                },
                height: 'parent',
                unselectAuto: false,

                axisFormat: 'HH:mm',
                // timeFormat: {
                //     agenda: 'HH:mm'
                // },
                slotDuration: '00:30:00',
                minTime: '09:00',
                maxTime: '21:00',
                resourceAreaWidth: '7%',
                resourceLabelText: 'Өргөгч',
                resources: JSON.parse('[{ "id": "1", "title": "1  Өргөгч01" },{ "id": "2", "title": "2  Өргөгч02" },{ "id": "3", "title": "3 " },{ "id": "4", "title": "4 " },{ "id": "5", "title": "5 " },{ "id": "6", "title": "6 " },{ "id": "7", "title": "7 " },{ "id": "8", "title": "8 " },{ "id": "9", "title": "9 " },{ "id": "10", "title": "10 " },{ "id": "11", "title": "11 " },{ "id": "12", "title": "12 " },{ "id": "13", "title": "13 " },{ "id": "14", "title": "14 " },{ "id": "15", "title": "15 " },{ "id": "16", "title": "16 " },{ "id": "17", "title": "17 " },{ "id": "18", "title": "18 " }]'),
                aspectRatio: 2.0,
                //allDaySlot:false,
            });

            this.$calendar.fullCalendar(fc_options);
        },
    });
});
