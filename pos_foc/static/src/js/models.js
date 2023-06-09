odoo.define('pos_foc.models', function (require) {
"use strict";
    const { Order, Orderline} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosFocOrderline = (Orderline) => class PosFocOrderline extends Orderline {
        constructor() {
            super(...arguments);
            this.is_foc = this.is_foc || false;
        }
        //@override
        can_be_merged_with(orderline) {
            if (orderline.is_foc != this.is_foc) {
                return false;
            } else {
                return super.can_be_merged_with(...arguments);
            }
        }
        //@override
        clone(){
            const orderline = super.clone(...arguments);
            orderline.is_foc = this.is_foc;
            return orderline;
        }
        //@override
        export_as_JSON(){
            const json = super.export_as_JSON(...arguments);
            json.is_foc = this.is_foc;
            return json;
        }
        //@override
        init_from_JSON(json){
            super.init_from_JSON(...arguments);
            this.is_foc = json.is_foc;
        }
        set_foc(foc){
            this.is_foc = foc;
        }
        get_foc(){
            return this.is_foc;
        }
    }
    Registries.Model.extend(Orderline, PosFocOrderline);

    const PosFocOrder = (Order) => class PosFocOrder extends Order {
        set_orderline_options(line, options) {
            super.set_orderline_options(...arguments);
            if (options && options.is_foc) {
                line.set_foc(options.is_foc);
            }
        }
    }
    Registries.Model.extend(Order, PosFocOrder);
});


    