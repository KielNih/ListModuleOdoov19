/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class StockDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            criticalProducts: [],
            totalCritical: 0,
        });
        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const result = await this.orm.call("product.product", "get_critical_stock_data", []);
        this.state.criticalProducts = result.products;
        this.state.totalCritical = result.total;
    }

    openCriticalProducts() {
        if (this.state.totalCritical === 0) return;
        const productIds = this.state.criticalProducts.map(p => p.id);
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Critical Stock Products",
            res_model: "product.product",
            views: [[false, "list"], [false, "form"]],
            domain: [['id', 'in', productIds]],
            target: "current",
        });
    }
}
StockDashboard.template = "custom_stock_dashboard.StockDashboardTemplate";
registry.category("actions").add("stock_threshold_dashboard", StockDashboard);