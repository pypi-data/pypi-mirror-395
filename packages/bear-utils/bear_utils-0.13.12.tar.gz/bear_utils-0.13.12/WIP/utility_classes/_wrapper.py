"""A Base wrapper class for objects."""

from io import StringIO
from typing import Self
from warnings import deprecated
from funcy_bear.exceptions import InputObjectError, OutputObjectError
from funcy_bear.type_stuffs.validate import type_param, validate_type


@deprecated("This class will be removed in future versions.")
class BaseWrapper[Incoming, Outgoing]:
    """A Base wrapper class for objects."""

    def __init__(self, incoming: Incoming | None, outgoing: Outgoing | None, **kwargs) -> None:
        """Initialize the BaseWrapper with a default value."""
        self._incoming_type: type[Incoming] = type_param(type(self), 0)
        self._outgoing_type: type[Outgoing] = type_param(type(self), 1)
        incoming = self._incoming_type() if incoming is None else incoming
        outgoing = self._outgoing_type() if outgoing is None else outgoing
        validate_type(incoming, self._incoming_type, InputObjectError)
        validate_type(outgoing, self._outgoing_type, OutputObjectError)
        self._root: Incoming = incoming
        self._cache: Outgoing = outgoing
        self.name: str = kwargs.get("name", "default")

    @property
    def root_obj(self) -> Incoming:
        """Get the root object."""
        return self._root

    @property
    def cache_obj(self) -> Outgoing:
        """Get the cached value."""
        return self._cache

    @cache_obj.setter
    def cache_obj(self, value: Outgoing) -> None:
        """Set the cached value."""
        validate_type(value, self._outgoing_type, OutputObjectError)
        self._cache = value


################################################################
################ EXAMPLE USAGE #################################
################################################################


@deprecated("This class will be removed in future versions.")
class StringIOWrapper(BaseWrapper[StringIO, str]):
    """A utility wrapper around the StringIO and str classes.

    The StringIOWrapper class provides a way to manage
    a StringIO object with caching capabilities. It allows
    writing to the StringIO object, caching its content,
    and resetting the object while optionally clearing the cache.
    It also has a fluent interface for chaining method calls.
    """

    def __init__(self, default_in: StringIO | None = None, default_out: str | None = None, **kwargs) -> None:
        """Initialize the StringIOWrapper with a StringIO object."""
        super().__init__(incoming=default_in, outgoing=default_out, **kwargs)

    def _reset(self, clear: bool = False) -> Self:
        """Reset the current IO object."""
        self.cache_obj: str = self.root_obj.getvalue()
        if clear:
            self.cache_obj = ""
        self.root_obj.truncate(0)
        self.root_obj.seek(0)
        return self

    def cache(self) -> Self:
        """Cache the current value of the IO object."""
        self.cache_obj = self.root_obj.getvalue()
        return self

    def reset(self, clear: bool = False) -> Self:
        """Will only reset the IO object but not the cached value.

        Args:
            clear (bool): If True, will clear the cached value.
        """
        self._reset(clear=clear)
        return self

    def write(self, *values: str) -> None:
        """Write values to the StringIO object."""
        for value in values:
            self.root_obj.write(value)

    def flush(self) -> None:
        """Save the current content to the cache and reset the StringIO object."""
        self._reset(clear=False)

    @property
    def empty_buffer(self) -> bool:
        """Check if the StringIO object is empty."""
        return not self.root_obj.getvalue()

    @property
    def empty_cache(self) -> bool:
        """Check if the cached value is empty."""
        return not self.cache_obj

    def getvalue(self, cache: bool = False) -> str:
        """Get the string value from the StringIO object."""
        if cache and self.empty_buffer:
            return self.cache_obj
        return self.root_obj.getvalue()

    def get_cache(self) -> str:
        """Get the cached value from the str object."""
        return self.cache_obj

    def __repr__(self) -> str:
        """Return a string representation of the StringIOWrapper."""
        return f"{self.__class__.__name__}(root_obj={self.root_obj.getvalue()}, cache_obj={self.cache_obj})"


__all__ = ["BaseWrapper", "StringIOWrapper"]
