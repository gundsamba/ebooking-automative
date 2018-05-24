odoo.define('fullcalendar.scheduler_model', function (require) {
    "use strict";

    var CalendarModel = require('web.CalendarModel');
    var core = require('web.core');
    var time = require('web.time');
    var scales = [
        'day',
        'week',
        'month',
        'timeline'
    ];
    var _t = core._t;

    CalendarModel.include({
        load: function (params) {
            var self = this;
            this.modelName = params.modelName;
            this.fields = params.fields;
            this.fieldNames = params.fieldNames;
            this.fieldsInfo = params.fieldsInfo;
            this.mapping = params.mapping;
            this.mode = params.mode;       // one of month, week or day
            this.scales = params.scales;   // one of month, week or day

            // Check whether the date field is editable (i.e. if the events can be
            // dragged and dropped)
            this.editable = params.editable;
            this.creatable = params.creatable;

            // display more button when there are too much event on one day
            this.eventLimit = params.eventLimit;

            // fields to display color, e.g.: user_id.partner_id
            this.fieldColor = params.fieldColor;
            if (!this.preload_def) {
                this.preload_def = $.Deferred();
                $.when(
                    this._rpc({model: this.modelName, method: 'check_access_rights', args: ["write", false]}),
                    this._rpc({model: this.modelName, method: 'check_access_rights', args: ["create", false]}))
                .then(function (write, create) {
                    self.write_right = write;
                    self.create_right = create;
                    self.preload_def.resolve();
                });
            }

            this.data = {
                domain: params.domain,
                context: params.context,
                // get in arch the filter to display in the sidebar and the field to read
                filters: params.filters,
            };

            this.setDate(params.initialDate);
            // Use mode attribute in xml file to specify zoom timeline (day,week,month)
            // by default month.
            this.setScale(params.mode);

            _.each(this.data.filters, function (filter) {
                if (filter.avatar_field && !filter.avatar_model) {
                    filter.avatar_model = self.modelName;
                }
            });

            return this.preload_def.then(this._loadCalendar.bind(this));
        },
        setDate: function (start) {
            console.log('setDate');
            this.data.start_date = this.data.end_date = this.data.target_date = this.data.highlight_date = start;
            this.data.start_date.utc().add(this.getSession().getTZOffset(this.data.start_date), 'minutes');
            console.log('this.data.scale : '+this.data.scale);
            console.log('start_date timeline: '+this.data.start_date.clone().startOf('timeline').format());
            console.log('end_date timeline: '+this.data.start_date.clone().endOf('timeline').format());

            switch (this.data.scale) {
                case 'month':
                    this.data.start_date = this.data.start_date.clone().startOf('month').startOf('week');
                    this.data.end_date = this.data.start_date.clone().add(5, 'week').endOf('week');
                    break;
                case 'week':
                    this.data.start_date = this.data.start_date.clone().startOf('week');
                    this.data.end_date = this.data.end_date.clone().endOf('week');
                    break;
                case 'day':
                    this.data.start_date = this.data.start_date.clone().startOf('day');
                    this.data.end_date = this.data.end_date.clone().endOf('day');
                    break;
                default:
                    this.data.start_date = this.data.start_date.clone().startOf('timeline');
                    this.data.end_date = this.data.end_date.clone().endOf('timeline');
            }
        },
        setScale: function (scale) {
            if (!_.contains(scales, scale)) {
                scale = "week";
            }
            this.data.scale = scale;
            this.setDate(this.data.target_date);
        },
        _getFullCalendarOptions: function () {
            return {
                defaultView: (this.mode === "month")? "month" : ((this.mode === "week")? "agendaWeek" : ((this.mode === "day")? "agendaDay" : ((this.mode === "timeline")? "timelineDay" : "timelineDay"))),
                header: false,
                selectable: this.creatable && this.create_right,
                selectHelper: true,
                editable: this.editable,
                droppable: true,
                navLinks: false,
                eventLimit: this.eventLimit, // allow "more" link when too many events
                snapMinutes: 15,
                longPressDelay: 500,
                eventResizableFromStart: true,
                weekNumbers: false,
                weekNumberTitle: _t("W"),
                allDayText: _t("All day"),
                views: {
                    week: {
                        columnFormat: 'ddd ' + time.getLangDateFormat(),
                        titleFormat: time.getLangTimeFormat(),
                    }
                },
                monthNames: moment.months(),
                monthNamesShort: moment.monthsShort(),
                dayNames: moment.weekdays(),
                dayNamesShort: moment.weekdaysShort(),
                firstDay: moment().startOf('week').isoWeekday(),
            };
        },
        /**
         * @returns {Deferred}
         */
        _loadCalendar: function () {
            var self = this;
            this.data.fullWidth = this.call('local_storage', 'getItem', 'calendar_fullWidth') === 'true';
            this.data.fc_options = this._getFullCalendarOptions();

            var defs = _.map(this.data.filters, this._loadFilter.bind(this));

            return $.when.apply($, defs).then(function () {
                return self._rpc({
                        model: self.modelName,
                        method: 'search_read',
                        context: self.data.context,
                        fields: self.fieldNames,
                        domain: self.data.domain.concat(self._getRangeDomain()).concat(self._getFilterDomain())
                })
                .then(function (events) {
                    self._parseServerData(events);
                    self.data.data = _.map(events, self._recordToCalendarEvent.bind(self));
                    return $.when(
                        self._loadColors(self.data, self.data.data),
                        self._loadRecordsToFilters(self.data, self.data.data)
                    );
                });
            });
        },
        /**
         * Transform OpenERP event object to fullcalendar event object
         */
        _recordToCalendarEvent: function (evt) {
            var date_start;
            var date_stop;
            var date_delay = evt[this.mapping.date_delay] || 1.0,
                all_day = this.mapping.all_day ? evt[this.mapping.all_day] : false,
                the_title = '',
                attendees = [];
            var resourceId = null;
            var view = this.data.scale;

            if (!all_day) {
                date_start = evt[this.mapping.date_start].clone();
                date_stop = this.mapping.date_stop ? evt[this.mapping.date_stop].clone() : null;
            } else {
                date_start = evt[this.mapping.date_start].clone().startOf('day');
                date_stop = this.mapping.date_stop ? evt[this.mapping.date_stop].clone().startOf('day') : null;
            }

            if (!date_stop && date_delay) {
                date_stop = date_start.clone().add(date_delay,'hours');
            }

            if (!all_day) {
                date_start.add(this.getSession().getTZOffset(date_start), 'minutes');
                date_stop.add(this.getSession().getTZOffset(date_stop), 'minutes');
            }

            if (this.mapping.all_day && evt[this.mapping.all_day]) {
                date_stop.add(1, 'days');
            }
            var isAllDay = this.fields[this.mapping.date_start].type === 'date' ||
                            this.mapping.all_day && evt[this.mapping.all_day] || false;
            var r = {
                'record': evt,
                'start': date_start,
                'end': date_stop,
                'r_start': date_start,
                'r_end': date_stop,
                'title': the_title,
                'allDay': isAllDay,
                'id': evt.id,
                'attendees':attendees,
                'resourceId':resourceId,
                'view':view,
            };

            if (this.mapping.all_day && evt[this.mapping.all_day]) {
                // r.start = date_start.format('YYYY-MM-DD');
                // r.end = date_stop.format('YYYY-MM-DD');
            } else if (this.data.scale === 'month' && this.fields[this.mapping.date_start].type !== 'date') {
                // In month, FullCalendar gives the end day as the
                // next day at midnight (instead of 23h59).
                date_stop.add(1, 'days');

                // allow to resize in month mode
                r.reset_allday = r.allDay;
                r.allDay = true;
                r.start = date_start.format('YYYY-MM-DD');
                r.end = date_stop.startOf('day').format('YYYY-MM-DD');
            }
            if (this.data.scale === 'timeline') {
                r.resourceId = evt.resource_id[0];
            }

            return r;
        },
    });
});
