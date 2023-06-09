odoo.define('pos_foc.FocProductManagementScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    const { useRef} = owl;

    class FocProductManagementScreen extends PosComponent {
        setup() {
            super.setup();
            this.searchWordInputRef = useRef('search-word-input-foc-product');
            this.state = {
                query: null,
            };
        }

        // Lifecycle hooks
        back() {
            this.showScreen('ProductScreen');
        }

        get products() {
            let list = [];
            let category = 0;
            if (this.state.query && this.state.query.trim() !== '') {
                list = this.env.pos.db.search_product_in_category(
                    category,
                    this.state.query.trim()
                );
            } else {
                list = this.env.pos.db.get_product_by_category(category);
            }
            list.forEach(function(prd) {
                prd['foc_image_url'] = '/web/image?model=product.product&field=image_128&id='+prd.id+'&unique='+prd.write_date;
            });
            return list.sort(function (a, b) { return a.display_name.localeCompare(b.display_name) });
        }

        async _onPressEnterKey() {
            if (!this.state.query) return;
            if (!this.env.pos.isEveryProductLoaded) {
                const result = await this.loadProductFromDB();
                this.showNotification(
                    _.str.sprintf(this.env._t('%s product(s) found for "%s".'),
                        result.length,
                        this.state.query)
                    , 3000);
                if (!result.length) this._clearSearch();
            }
        }
        _clearSearch() {
            this.searchWordInputRef.el.value = '';
            this.state.query = '';
            this.render(true);
        }
        async updateProductList(event) {
            this.state.query = event.target.value;
            if (event.code === 'Enter') {
                this._onPressEnterKey();
            } else {
                this.render(true);
            }
        }

        async loadProductFromDB() {
            if(!this.state.query)
                return;

            try {
                let ProductIds = await this.rpc({
                    model: 'product.product',
                    method: 'search',
                    args: [['&',['available_in_pos', '=', true], '|','|','|',
                     ['name', 'ilike', this.state.query],
                     ['default_code', 'ilike', this.state.query],
                     ['barcode', 'ilike', this.state.query]]],
                    context: this.env.session.user_context,
                });
                if(ProductIds.length) {
                    if (!this.env.pos.isEveryProductLoaded) await this.env.pos.updateIsEveryProductLoaded();
                    await this.env.pos._addProducts(ProductIds, false);
                }
                this.render(true);
                return ProductIds;
            } catch (error) {
                const identifiedError = identifyError(error)
                if (identifiedError instanceof ConnectionLostError || identifiedError instanceof ConnectionAbortedError) {
                    return this.showPopup('OfflineErrorPopup', {
                        title: this.env._t('Network Error'),
                        body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                    });
                } else {
                    throw error;
                }
            }
        }

        click_on_foc_product(event) {
            var self = this;
            var product_id = parseInt(event.currentTarget.dataset['productId'])
            var orderlines = self.env.pos.get_order().get_orderlines();
            if (orderlines && orderlines.length >= 1){
                self.env.pos.get_order().add_product(self.env.pos.db.product_by_id[product_id],
                {
                  is_foc: true,
                  quantity: 1,
                  price: 0,
                  extras: {price_manually_set: true},
                });
            }
            else{
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t("No product in cart."),
                });
            }
            this.showScreen('ProductScreen');
        }
    }
    FocProductManagementScreen.template = 'FocProductManagementScreen';

    Registries.Component.add(FocProductManagementScreen);

    return FocProductManagementScreen;
});
