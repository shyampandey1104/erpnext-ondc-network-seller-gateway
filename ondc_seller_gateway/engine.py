"""ONDC (Open Network for Digital Commerce) Beckn Protocol Seller Gateway Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class BecknCatalogItem:
    item_id: str
    item_name: str
    category_id: str
    price_inr: float
    available_stock_qty: int
    seller_gstin: str
    fulfillment_type: str = "Delivery"  # Delivery, Pickup

@dataclass
class BecknOrderTransaction:
    transaction_id: str
    bap_id: str                          # Buyer App Platform ID
    bpp_id: str                          # Seller App Platform ID
    item_id: str
    quantity: int
    total_order_amount_inr: float
    delivery_pincode: str
    status: str = "CREATED"              # CREATED, CONFIRMED, IN_TRANSIT, DELIVERED, CANCELLED

class ONDCSellerGatewayEngine:
    def __init__(self, seller_bpp_id: str, seller_gstin: str):
        self.seller_bpp_id = seller_bpp_id
        self.seller_gstin = seller_gstin
        self.catalog: Dict[str, BecknCatalogItem] = {}
        self.orders: Dict[str, BecknOrderTransaction] = {}

    def publish_catalog_item(self, item: BecknCatalogItem) -> Dict[str, Any]:
        self.catalog[item.item_id] = item
        return {"item_id": item.item_id, "status": "PUBLISHED_ON_ONDC"}

    def handle_search_intent(self, category_id: Optional[str] = None, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
        results = []
        for it in self.catalog.values():
            if category_id and it.category_id != category_id:
                continue
            if max_price and it.price_inr > max_price:
                continue
            if it.available_stock_qty > 0:
                results.append({
                    "item_id": it.item_id,
                    "item_name": it.item_name,
                    "price": it.price_inr,
                    "stock": it.available_stock_qty,
                    "bpp_id": self.seller_bpp_id
                })
        return results

    def process_on_confirm_order(self, order: BecknOrderTransaction) -> Dict[str, Any]:
        if order.item_id not in self.catalog:
            raise ValueError(f"Item {order.item_id} not available on BPP {self.seller_bpp_id}.")
        item = self.catalog[order.item_id]
        if order.quantity > item.available_stock_qty:
            raise ValueError(f"Insufficient stock! Available: {item.available_stock_qty}, Requested: {order.quantity}")

        expected_total = round(item.price_inr * order.quantity, 2)
        item.available_stock_qty -= order.quantity
        order.status = "CONFIRMED"
        order.total_order_amount_inr = expected_total
        self.orders[order.transaction_id] = order

        return {
            "transaction_id": order.transaction_id,
            "order_status": "CONFIRMED",
            "total_value_inr": expected_total,
            "logistics_handshake_ready": True
        }
