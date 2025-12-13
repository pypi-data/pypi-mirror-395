"""Basic data types."""

from typing import Annotated, NewType

from msgspec import Struct, Meta

__all__ = [
    "CustomerId", "CartId", "CartItem", "Cart", "CartTotal", "CalculatedCart", "CalculatedCartItem"
]

CustomerId = NewType("CustomerId", int)
CartId = NewType("CartId", str)

class CartItem(Struct):
    """Raw cart item as in db."""
    id: str                 #: product id
    quantity: Annotated[int, Meta(ge=1)]
    picked: bool = True     #: customer selected this item as active for order

class Cart(Struct):
    """Raw cart data as in db."""
    updated: int
    items: list[CartItem]

class CalculatedCartItem(Struct):
    """Cart item with calculated values for a particular store."""
    id: str         #: product id
    quantity: int
    picked: bool    #: customer selected this item as active for order
    price: int      #: actual price per item
    price_old: int  #: base price per item
    discount: int   #: difference between `price` and `price_old`
    available_quantity: int     #: quantity available in the selected store

class CartTotal(Struct):
    price: int
    quantity: int
    discount: int
    price_old: int

class CalculatedCart(Struct):
    """Cart with calculated values for a particular store."""
    id: CartId
    store_id: str       #: selected store
    total: CartTotal    #: total values for all the cart items
    items: list[CalculatedCartItem]
    items_not_available: list[CartItem]
