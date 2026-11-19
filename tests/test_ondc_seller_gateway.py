import unittest
from ondc_seller_gateway.engine import BecknCatalogItem, BecknOrderTransaction, ONDCSellerGatewayEngine

class TestONDCSellerGatewayEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ONDCSellerGatewayEngine(seller_bpp_id="bpp.samwadini.com", seller_gstin="07AAAAA0000A1Z5")
        self.engine.publish_catalog_item(BecknCatalogItem(
            item_id="SKU-ORGANIC-ATTA-5KG", item_name="Stone Ground Whole Wheat Atta 5kg",
            category_id="Grocery", price_inr=320.0, available_stock_qty=50, seller_gstin="07AAAAA0000A1Z5"
        ))

    def test_search_discovery(self):
        res = self.engine.handle_search_intent(category_id="Grocery", max_price=400.0)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["item_id"], "SKU-ORGANIC-ATTA-5KG")

    def test_order_confirmation_and_stock_deduction(self):
        order = BecknOrderTransaction(
            transaction_id="TXN-ONDC-2026-9901", bap_id="buyerapp.paytm.com",
            bpp_id="bpp.samwadini.com", item_id="SKU-ORGANIC-ATTA-5KG",
            quantity=2, total_order_amount_inr=0.0, delivery_pincode="110001"
        )
        conf = self.engine.process_on_confirm_order(order)
        self.assertEqual(conf["order_status"], "CONFIRMED")
        self.assertEqual(conf["total_value_inr"], 640.0)
        self.assertEqual(self.engine.catalog["SKU-ORGANIC-ATTA-5KG"].available_stock_qty, 48)

if __name__ == "__main__":
    unittest.main()
