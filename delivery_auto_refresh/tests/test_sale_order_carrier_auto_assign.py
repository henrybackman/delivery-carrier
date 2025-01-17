# Copyright 2024 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

# MIGRATION NOTE for 17.0: Move this to module sale_order_carrier_auto_assign

from odoo.tests import Form, TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestSaleOrderCarrierAutoAssignCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env["base"].with_context(**DISABLED_MAIL_CONTEXT).env

        cls.partner = cls.env.ref("base.res_partner_2")
        cls.product_storable = cls.env.ref("product.product_product_9")
        cls.delivery_local_delivery = cls.env.ref("delivery.delivery_local_delivery")
        cls.delivery_local_delivery.fixed_price = 10


class TestSaleOrderCarrierAutoAssignOnCreate(TestSaleOrderCarrierAutoAssignCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.settings = cls.env["res.config.settings"].create({})

    def test_sale_order_carrier_auto_assign_onchange(self):
        self.assertEqual(
            self.partner.property_delivery_carrier_id, self.delivery_local_delivery
        )
        self.settings.sale_auto_assign_carrier_on_create = True
        self.settings.set_values()
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.partner
        sale_order = sale_order_form.save()
        self.assertEqual(sale_order.carrier_id, self.delivery_local_delivery)

    def test_sale_order_carrier_auto_assign_create(self):
        self.assertEqual(
            self.partner.property_delivery_carrier_id, self.delivery_local_delivery
        )
        self.settings.sale_auto_assign_carrier_on_create = True
        self.settings.set_values()
        sale_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        self.assertEqual(sale_order.carrier_id, self.delivery_local_delivery)

    def test_sale_order_carrier_auto_assign_disabled(self):
        self.assertEqual(
            self.partner.property_delivery_carrier_id, self.delivery_local_delivery
        )
        self.settings.sale_auto_assign_carrier_on_create = False
        self.settings.set_values()
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.partner
        sale_order = sale_order_form.save()
        self.assertFalse(sale_order.carrier_id)

    def test_sale_order_carrier_auto_assign_no_carrier(self):
        self.partner.property_delivery_carrier_id = False
        self.settings.sale_auto_assign_carrier_on_create = True
        self.settings.set_values()
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.partner
        sale_order = sale_order_form.save()
        self.assertFalse(sale_order.carrier_id)

    def test_sale_order_carrier_auto_assign_carrier_already_set(self):
        self.assertEqual(
            self.partner.property_delivery_carrier_id, self.delivery_local_delivery
        )
        self.settings.sale_auto_assign_carrier_on_create = True
        carrier = self.env.ref("delivery.delivery_carrier")
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "carrier_id": carrier.id,
            }
        )
        self.assertEqual(sale_order.carrier_id, carrier)
