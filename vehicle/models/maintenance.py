from odoo import fields, models, api, _


class MaintenanceServices(models.Model):
    _name = "maintenance.services"
    _description = "Maintenance Services"

    name = fields.Char(string="Service Name")
    maintenance_id = fields.Many2one("maintenance.records", string="Maintenance Record")
    # Add other fields as needed

    service_date = fields.Date(string="Date")
    service_id = fields.Many2one(
        "product.product", string="Service", domain=[("type", "=", "service")]
    )
    quantity = fields.Float(string="Quantity")

    discount = fields.Float(string="Discount")
    total = fields.Float(string="Total", compute="_compute_total")
    price = fields.Float(string="Price", compute="_compute_price")

    @api.depends("quantity", "price", "discount")
    def _compute_total(self):
        for record in self:
            record.total = (record.quantity * record.price) - record.discount

    @api.depends("service_id")
    def _compute_price(self):
        for record in self:
            if record.service_id:
                record.price = record.service_id.lst_price
            else:
                record.price = 0.0


class SpareParts(models.Model):
    _name = "maintenance.spares"
    _description = "Spare Parts"

    name = fields.Char(string="Product Name")
    maintenance_id = fields.Many2one("maintenance.records", string="Maintenance Record")
    # Add other fields as needed

    spare_date = fields.Date(string="Date")
    spare_id = fields.Many2one(
        "product.product", string="Product", domain=[("type", "=", "consumable")]
    )
    spare_quantity = fields.Float(string="Quantity")
    spare_discount = fields.Float(string="Discount")
    spare_total = fields.Float(string="Total", compute="_compute_total")
    spare_price = fields.Float(string="Price", compute="_compute_price")

    @api.depends("spare_quantity", "spare_price", "spare_discount")
    def _compute_total(self):
        for record in self:
            record.spare_total = (
                record.spare_quantity * record.spare_price
            ) - record.spare_discount

    @api.depends("spare_id")
    def _compute_price(self):
        for record in self:
            if record.spare_id:
                record.spare_price = record.spare_id.lst_price
            else:
                record.spare_price = 0.0


class MaintenanceDetails(models.Model):
    _name = "maintenance.records"
    _description = "Maintenance Details"
    _inherit = "mail.thread"

    name = fields.Char(string="Reference")
    employee_name = fields.Char(string="Employee Name * ", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer")
    vehicle_id = fields.Many2one(
        "vehicles.master",
        string="Vehicle",
        widget="many2one",
    )
    ref = fields.Char(string="Sequence", default=lambda self: _("New"))
    active = fields.Boolean(default=True)
    maintenance_date = fields.Date(string="Date")
    services_ids = fields.One2many(
        "maintenance.services", "maintenance_id", string="Maintenance Details"
    )
    spare_ids = fields.One2many(
        "maintenance.spares", "maintenance_id", string="Spare Parts Details"
    )
    # total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    # For calculating the total amount the service and spare parts details ( SATARTS HERE)
    total_services_amount = fields.Float(
        string="Total Services Amount", compute="_compute_total_services_amount"
    )
    total_products_amount = fields.Float(
        string="Total Products Amount", compute="_compute_total_products_amount"
    )
    net_total = fields.Float(string="Net Total Amount", compute="_compute_total_amount")
    maintenance_information = fields.Html(string="Comments")

    @api.depends("services_ids.total")
    def _compute_total_services_amount(self):
        for record in self:
            record.total_services_amount = sum(record.services_ids.mapped("total"))

    @api.depends("spare_ids.spare_total")
    def _compute_total_products_amount(self):
        for record in self:
            record.total_products_amount = sum(record.spare_ids.mapped("spare_total"))

    @api.depends("total_services_amount", "total_products_amount")
    def _compute_total_amount(self):
        for record in self:
            record.net_total = (
                record.total_services_amount + record.total_products_amount
            )

    # #For calculating the total amount the service and spare parts details ( ENDS HERE)

    def _get_default_stage(self):
        default_stage = self.env["maintenance.stage"].search(
            [], limit=1, order="sequence"
        )
        return default_stage

    stage_id = fields.Many2one(
        "maintenance.stage", string="Stage", default=_get_default_stage
    )

    def name_get(self):
        result = []
        for record in self:
            name = "{} - {}".format(record.customer_id.phone, record.customer_id.mobile)
            result.append((record.id, name))
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("maintenance.records")
        return super(MaintenanceDetails, self).create(vals_list)
