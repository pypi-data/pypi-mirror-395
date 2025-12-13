"""
Pagination utilities for Python SDK.

Provides PaginatedData class for wrapping paginated responses with helper methods.
"""

from typing import TypeVar, Generic, Callable, Awaitable, Any

# FinaticResponse is Dict[str, Any] in generated types
# Use string annotation to avoid circular import
FinaticResponse = "Dict[str, Any]"

T = TypeVar("T")


class PaginationMeta:
    """Pagination metadata from API response."""

    def __init__(self, has_more: bool, next_offset: int | None, current_offset: int, limit: int):
        self.has_more = has_more
        self.next_offset = next_offset
        self.current_offset = current_offset
        self.limit = limit


class PaginatedData(Generic[T]):
    """
    PaginatedData wraps a data array with pagination metadata and helper methods.

    Generic parameter T is the element type (e.g., FDXBrokerAccount).

    This class behaves like a list, so you can use it directly as an array:
    - len(paginated_data) returns the number of items
    - paginated_data[0] returns the first item
    - for item in paginated_data: iterates over items
    - paginated_data.length (property) returns the number of items

    It also provides pagination methods:
    - has_more: Check if there are more pages
    - next_page(): Get the next page
    - prev_page(): Get the previous page
    - first_page(): Get the first page
    - last_page(): Get the last page

    Usage:
    ```python
    response = await sdk.get_accounts()
    accounts = response.success["data"]  # Can use directly as array!
    print(len(accounts))  # Works directly
    print(accounts[0])  # Works directly
    for account in accounts:  # Works directly
        print(account)

    if accounts.has_more:
        next_page = await accounts.next_page()  # Returns PaginatedData[FDXBrokerAccount]
        next_accounts = next_page  # Can use directly as array too!
    ```
    """

    def __init__(
        self,
        items: list[T],  # The actual data array
        meta: PaginationMeta,
        original_method: Callable[..., Awaitable[Any]],  # Returns FinaticResponse[PaginatedData[T]]
        current_params: dict[str, Any],
        wrapper_instance: Any,
    ):
        self.items = items
        self.meta = meta
        self._original_method = original_method
        self._current_params = current_params
        self._wrapper_instance = wrapper_instance

    def __len__(self) -> int:
        """Return the number of items (allows len(paginated_data))."""
        return len(self.items)

    def __getitem__(self, index: int | slice) -> T | list[T]:
        """Allow indexing (allows paginated_data[0] and paginated_data[0:5])."""
        return self.items[index]

    def __iter__(self):
        """Allow iteration (allows for item in paginated_data)."""
        return iter(self.items)

    def __repr__(self) -> str:
        """String representation showing it's a paginated array."""
        return f"<PaginatedData[{len(self.items)} items, has_more={self.meta.has_more}]>"

    @property
    def length(self) -> int:
        """Get the number of items (property access for consistency)."""
        return len(self.items)

    @property
    def has_more(self) -> bool:
        """Check if there are more pages available."""
        return self.meta.has_more

    # Array-like methods - delegate to items list
    def for_each(self, callback):
        """
        Calls a function for each element in the list.

        Args:
            callback: Function to call for each item (item, index)
        """
        for index, item in enumerate(self.items):
            callback(item, index)

    def map(self, callback):
        """
        Creates a new list with the results of calling a function for every list element.

        Args:
            callback: Function to call for each item (item, index) -> new_value

        Returns:
            New list with transformed values
        """
        return [callback(item, index) for index, item in enumerate(self.items)]

    def filter(self, callback):
        """
        Returns the elements of a list that meet the condition specified in a callback function.

        Args:
            callback: Function to test each item (item, index) -> bool

        Returns:
            New list with filtered items
        """
        return [item for index, item in enumerate(self.items) if callback(item, index)]

    def find(self, predicate):
        """
        Returns the value of the first element in the list where predicate is true.

        Args:
            predicate: Function to test each item (item, index) -> bool

        Returns:
            First matching item or None
        """
        for index, item in enumerate(self.items):
            if predicate(item, index):
                return item
        return None

    def find_index(self, predicate):
        """
        Returns the index of the first element in the list where predicate is true.

        Args:
            predicate: Function to test each item (item, index) -> bool

        Returns:
            Index of first matching item or -1
        """
        for index, item in enumerate(self.items):
            if predicate(item, index):
                return index
        return -1

    def includes(self, search_element: T) -> bool:
        """
        Determines whether a list includes a certain element.

        Args:
            search_element: Element to search for

        Returns:
            True if element is found, False otherwise
        """
        return search_element in self.items

    def index_of(self, search_element: T, from_index: int = 0) -> int:
        """
        Returns the index of the first occurrence of a value in a list.

        Args:
            search_element: Element to search for
            from_index: Starting index (default: 0)

        Returns:
            Index of first occurrence or -1
        """
        try:
            return self.items.index(search_element, from_index)
        except ValueError:
            return -1

    def to_dict(self) -> list[T]:
        """
        Return the items array as a list (for JSON serialization).

        This allows clean serialization without exposing internal methods.
        Use with json.dumps() default parameter for automatic serialization.

        Returns:
            The items array

        Example:
            >>> import json
            >>> orders = await sdk.get_orders()
            >>> print(orders)  # Shows full PaginatedData with methods
            >>> print(orders.to_dict())  # Shows just the items array
            >>> json.dumps(orders, default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else o.__dict__)
        """
        return self.items

    async def next_page(self) -> "PaginatedData[T]":
        """
        Get the next page of data.

        Returns:
            PaginatedData[T]: The next page (not wrapped in FinaticResponse)

        Raises:
            ValueError: If no more pages are available or fetch fails
        """
        if not self.has_more:
            raise ValueError("No more pages available")
        if self.meta.next_offset is None:
            raise ValueError("Next offset is null")
        new_params = {**self._current_params, "offset": self.meta.next_offset}
        response = await self._original_method(**new_params)
        if not response.get("success"):
            error_msg = (
                response.get("error", {}).get("message", "Failed to fetch next page")
                if response.get("error")
                else "Failed to fetch next page"
            )
            raise ValueError(error_msg)
        return response["success"]["data"]  # Return PaginatedData directly

    async def prev_page(self) -> "PaginatedData[T]":
        """
        Get the previous page of data.

        Returns:
            PaginatedData[T]: The previous page (not wrapped in FinaticResponse)

        Raises:
            ValueError: If fetch fails
        """
        prev_offset = max(0, self.meta.current_offset - self.meta.limit)
        new_params = {**self._current_params, "offset": prev_offset}
        response = await self._original_method(**new_params)
        if not response.get("success"):
            error_msg = (
                response.get("error", {}).get("message", "Failed to fetch previous page")
                if response.get("error")
                else "Failed to fetch previous page"
            )
            raise ValueError(error_msg)
        return response["success"]["data"]  # Return PaginatedData directly

    async def first_page(self) -> "PaginatedData[T]":
        """
        Get the first page of data.

        Returns:
            PaginatedData[T]: The first page (not wrapped in FinaticResponse)

        Raises:
            ValueError: If fetch fails
        """
        new_params = {**self._current_params, "offset": 0}
        response = await self._original_method(**new_params)
        if not response.get("success"):
            error_msg = (
                response.get("error", {}).get("message", "Failed to fetch first page")
                if response.get("error")
                else "Failed to fetch first page"
            )
            raise ValueError(error_msg)
        return response["success"]["data"]  # Return PaginatedData directly

    async def last_page(self) -> "PaginatedData[T]":
        """
        Get the last page of data.
        Uses iterative approach to find the last page.

        Returns:
            PaginatedData[T]: The last page (not wrapped in FinaticResponse)

        Raises:
            ValueError: If fetch fails
        """
        # Iterative approach to find last page
        current_offset = self.meta.current_offset
        last_valid_data: PaginatedData[T] | None = None

        while True:
            test_params = {**self._current_params, "offset": current_offset}
            response = await self._original_method(**test_params)
            if not response.get("success"):
                break
            last_valid_data = response["success"]["data"]
            if not last_valid_data or not last_valid_data.has_more:
                break
            current_offset += self.meta.limit

        if not last_valid_data:
            raise ValueError("Failed to fetch last page")

        return last_valid_data  # Return PaginatedData directly
