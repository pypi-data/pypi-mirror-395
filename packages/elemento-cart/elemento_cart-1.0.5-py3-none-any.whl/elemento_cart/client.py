from typing import overload

from msgspec import convert

from kaiju_tools.http import RPCClientService

from .types import *


class ElementoCartClient(RPCClientService):
    """Auto-generated ElementoCart RPC client."""

    @overload
    async def carts_get_cart(
        self, cart_id: str, store_id: str,
        _max_timeout: int = None
    ) -> CalculatedCart | None:
        ...

    @overload
    async def carts_get_cart(
        self, cart_id: str, store_id: None,
        _max_timeout: int = None
    ) -> Cart | None:
        ...

    async def carts_get_cart(
        self, cart_id: str, store_id: str = None,
        _max_timeout: int = None
    ):
        """Get a cart.

        :param cart_id:
        :param store_id: store and price channel id
        :return: calculated cart if `store_id` provided, simple cart otherwise, `None` if the cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.get',
            params=dict(cart_id=cart_id, store_id=store_id),
            max_timeout=_max_timeout
        )
        if not cart:
            return None
        if store_id is None:
            return convert(cart, type=Cart)
        return convert(cart, type=CalculatedCart)

    async def carts_set_cart(
        self, items: list[CartItem], store_id: str, cart_id: str = None,
        _max_timeout: int = None, _nowait: bool = False
    ) -> CalculatedCart | None:
        """Set a cart with new items.

        :param cart_id: identifier or `None` to create a cart with a new id
        :param items: list of items with id and quantity
        :param store_id: store and price channel id
        :return: calculated cart, `None` if the cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.set',
            params=dict(items=items, store_id=store_id, cart_id=cart_id),
            max_timeout=_max_timeout,
            nowait=_nowait
        )
        if not cart:
            return None
        return convert(cart, type=CalculatedCart)

    async def carts_delete_cart(
        self, cart_id: str,
        _max_timeout: int = None, _nowait: bool = False
    ) -> None:
        """Delete a cart and its items."""
        await self.call(
            method='carts.delete',
            params=dict(cart_id=cart_id),
            max_timeout=_max_timeout,
            nowait=_nowait
        )

    async def carts_add_items_to_cart(
        self, cart_id: str, items: list[CartItem], store_id: str,
        _max_timeout: int = None, _nowait: bool = False
    ) -> CalculatedCart | None:
        """Add new items to a cart.

        :param cart_id: identifier
        :param items: list of items with id and quantity
        :param store_id: store and price channel id
        :return: calculated cart, `None` if the cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.add',
            params=dict(cart_id=cart_id, items=items, store_id=store_id),
            max_timeout=_max_timeout,
            nowait=_nowait
        )
        if not cart:
            return None
        return convert(cart, type=CalculatedCart)

    async def carts_subtract_items_from_cart(
        self, cart_id: str, items: list[CartItem], store_id: str,
        _max_timeout: int = None, _nowait: bool = False
    ) -> CalculatedCart | None:
        """Remove items from a cart.

        Item quantities will be subtracted. If an item quantity reaches zero - item will be removed.

        :param cart_id: identifier
        :param items: list of items with quantities to subtract
        :param store_id: store and price channel id
        :return: calculated cart, `None` if the cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.sub',
            params=dict(cart_id=cart_id, items=items, store_id=store_id),
            max_timeout=_max_timeout,
            nowait=_nowait
        )
        if not cart:
            return None
        return convert(cart, type=CalculatedCart)

    @overload
    async def carts_get_customer_cart(
        self, customer_id: int, store_id: str,
        _max_timeout: int = None
    ) -> CalculatedCart | None:
        ...

    @overload
    async def carts_get_customer_cart(
        self, customer_id: int, store_id: None,
        _max_timeout: int = None
    ) -> Cart | None:
        ...

    async def carts_get_customer_cart(
        self, customer_id: int, store_id: str = None,
        _max_timeout: int = None
    ):
        """Get a customer cart.

        :param customer_id: customer identifier
        :param store_id: store and price channel id
        :return: calculated cart if `store_id` provided, simple cart otherwise, `None` if the cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.customer.get',
            params=dict(customer_id=customer_id, store_id=store_id),
            max_timeout=_max_timeout
        )
        if not cart:
            return None
        if store_id is None:
            return convert(cart, type=Cart)
        return convert(cart, type=CalculatedCart)

    async def carts_move_cart_to_customer(
        self, cart_id: str, customer_id: int, store_id: str, merge: bool = True,
        _max_timeout: int = None, _nowait: bool = False
    ) -> CalculatedCart | None:
        """Move a cart to a customer cart.

        :param cart_id: identifier
        :param customer_id: customer identifier
        :param store_id: store and price channel id
        :param merge: whether to merge cart into an existing one (otherwise it will be replaced)
        :return: calculated customer-bound cart, `None` if both carts don't exist or empty,
            customer cart as-is if the first cart doesn't exist or empty
        """
        cart = await self.call(
            method='carts.customer.move_to',
            params=dict(cart_id=cart_id, customer_id=customer_id, store_id=store_id, merge=merge),
            max_timeout=_max_timeout,
            nowait=_nowait
        )
        if not cart:
            return None
        return convert(cart, type=CalculatedCart)
