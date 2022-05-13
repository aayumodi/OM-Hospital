odoo.define('ehcs_web.clock', function (require) {
    "use strict";
    var core = require('web.core');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    var WebClock = Widget.extend({
        template: "web_clock",

        init: function() {
            this._super.apply(this, arguments);
            setInterval(function() {this.$("#submitBtn").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));}, 500);
        },
    });
    SystrayMenu.Items.push(WebClock);
    return WebClock;
});
