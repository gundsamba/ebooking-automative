odoo.define('ebooking_auto.base', function (require) {
    "use strict";
    var RelationalFields = require('web.relational_fields');
    var core = require('web.core');
    var qweb = core.qweb;

    RelationalFields.FieldStatus.include({
        _render: function () {
            var self = this;
            var model = self.model;
            var selections = _.partition(this.status_information, function (info) {
                return (info.selected || !info.fold);
            });
            var rowIndex = 0;
            var qweb_name = "FieldStatus.content";
            _.each(selections[0], function (record) {
                if(model == 'ebooking_auto.appointment'){
                    if(record.id == 'order') record.under_color = '#4c4f53';
                    else if(record.id == 'wait') record.under_color = '#ac5287 ';
                    else if(record.id == 'serve') record.under_color = '#f0ad4e';
                    else if(record.id == 'complete') record.under_color = '#337ab7';
                    else if(record.id == 'paid') record.under_color = '#5cb85c';
                    else if(record.id == 'cancel') record.under_color = '#d9534f';
                    selections[0][rowIndex] = record;
                    rowIndex++;
                }
            });
            if(model == 'ebooking_auto.appointment'){
                qweb_name = "ebooking_auto.FieldStatus.content";
            }
            this.$el.html(qweb.render(qweb_name, {
                selection_unfolded: selections[0],
                selection_folded: selections[1],
                clickable: !!this.attrs.clickable,
            }));
        },
    });
});
