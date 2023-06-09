odoo.define('pos_foc.PosFocButton', function(require) {
    "use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');

    class PosFocButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        async onClick() {
            let self = this;
            Gui.showScreen('FocProductManagementScreen');
        }
    }
    PosFocButton.template = 'PosFocButton';
    ProductScreen.addControlButton({
        component: PosFocButton,
        condition: function() {
            return true;
        },
    });
    Registries.Component.add(PosFocButton);
    return PosFocButton;

});


    