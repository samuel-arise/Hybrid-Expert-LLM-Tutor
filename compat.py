# compat.py
# Must be imported before experta or frozendict in every file that uses them.
import collections
import collections.abc

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable

if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping

if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping

if not hasattr(collections, "Iterable"):
    collections.Iterable = collections.abc.Iterable

if not hasattr(collections, "Iterator"):
    collections.Iterator = collections.abc.Iterator