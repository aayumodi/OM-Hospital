odoo.define("om_hospital.date", function (require){
	"use strict";

	// alert("Loaded")
	console.log("loaded again")
	// debugger;
	var FieldDate = require('web.basic_fields').FieldDate;
    FieldDate.include({
        init: function () {
            this._super.apply(this, arguments);
            if (this.nodeOptions.disable_past_date) {
                var d = new Date();
                d.setHours(0,0,0,0);
                this.datepickerOptions['minDate'] = moment(d);
            }
        }
    });

});