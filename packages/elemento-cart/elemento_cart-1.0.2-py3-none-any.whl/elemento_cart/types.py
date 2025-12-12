"""Basic data types."""

from typing import Annotated, NewType

from msgspec import Struct, Meta

__all__ = [
    "CustomerId", "CartId", "CartItem", "Cart", "CartTotal", "CalculatedCart", "CalculatedCartItem"
]

CustomerId = NewType("CustomerId", int)
CartId = NewType("CartId", str)

class CartItem(Struct):
    id: str
    quantity: Annotated[int, Meta(ge=1)]
    picked: bool = True

class Cart(Struct):
    items: list[CartItem]

class CalculatedCartItem(Struct):
    id: str
    quantity: int
    picked: bool
    price: int
    price_old: int
    discount: int
    available_quantity: int

class CartTotal(Struct):
    price: int
    quantity: int
    discount: int
    price_old: int

class CalculatedCart(Struct):
    id: CartId
    store_id: str
    total: CartTotal
    items: list[CalculatedCartItem]
    items_not_available: list[CartItem]

