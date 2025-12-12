from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Union,
)


def append_values(x: Dict[Any, List], y: Mapping) -> Dict[Any, List]:
    """
    Append values to a dictionary of lists.

    Args:
        x: Dictionary to append to.
        y: Values to append.

    Returns:
        Input dictionary :code:`x` with values of :code:`y` appended.

    Examples:

        >>> from collectiontools import append_values
        >>>
        >>> x = {}
        >>> append_values(x, {"a": 1, "b": "c"})
        {'a': [1], 'b': ['c']}
        >>> append_values(x, {"a": 2, "b": "d"})
        {'a': [1, 2], 'b': ['c', 'd']}
    """
    for key, value in y.items():
        x.setdefault(key, []).append(value)
    return x


def filter_values(predicate: Callable, x: dict) -> dict:
    """
    Filter a dictionary by values like :func:`filter` for iterables.

    Args:
        predicate: Predicate to evaluate on values of :code:`x`. Values are included if
            :code:`predicate` evaluates to :code:`True`.
        x: Dictionary to filter.

    Returns:
        Filtered dictionary.

    Examples:

        >>> from collectiontools import filter_values
        >>>
        >>> filter_values(lambda x: isinstance(x, int), {"a": 1, "b": 2, "c": "hello"})
        {'a': 1, 'b': 2}
    """
    return {key: value for key, value in x.items() if predicate(value)}


def map_values(func: Callable, x: dict, recursive: bool = False) -> dict:
    """
    Map a function over values of a dictionary like :func:`map` for iterables.

    Args:
        func: Function to apply to values of :code:`x`.
        x: Dictionary whose values to map :code:`func` over.
        recursive: Apply :code:`func` recursively to nested dictionaries.

    Returns:
        Dictionary with values obtained by applying :code:`func` to the values of
        :code:`x`.

    Examples:

        >>> from collectiontools import map_values
        >>>
        >>> map_values(lambda x: 2 * x, {"a": 1, "b": "hello"})
        {'a': 2, 'b': 'hellohello'}
        >>>
        >>> map_values(lambda x: 2 * x, {"a": {"b": 3}}, recursive=True)
        {'a': {'b': 6}}
    """
    return {
        key: (
            map_values(func, value, recursive)
            if recursive and isinstance(value, dict)
            else func(value)
        )
        for key, value in x.items()
    }


def transpose(x: Union[Mapping, Iterable]) -> Union[dict, list]:
    """
    Transpose between iterables of mappings and mappings of iterables.

    Args:
        x: Iterable of mappings or mapping of iterables to transpose.

    Returns:
        Transposed mapping of iterables or iterable of mappings.

    .. seealso::

        Transposition is implemented by :func:`transpose_to_dict` and
        :func:`transpose_to_list`.

    Examples:

        >>> from collectiontools import transpose
        >>>
        >>> x = [{"a": 1, "b": "hello"}, {"a": 2, "b": "hello"}]
        >>> y = transpose(x)
        >>> y
        {'a': [1, 2], 'b': ['hello', 'hello']}
        >>> transpose(y) == x
        True
    """
    if isinstance(x, Mapping):
        return transpose_to_list(x)
    elif isinstance(x, Iterable):
        return transpose_to_dict(x)
    else:
        raise ValueError(f"Value must be a mapping or iterable but got {x}.")


def transpose_to_dict(x: Iterable[Mapping]) -> Dict[Any, List]:
    """
    Transpose an iterable of mappings to a dictionary of lists.

    Args:
        x: Iterable to transpose.

    Returns:
        Dictionary of lists.

    Examples:

        >>> from collectiontools import transpose_to_dict
        >>>
        >>> transpose_to_dict([{"a": 1, "b": "hello"}, {"a": 2, "b": "hello"}])
        {'a': [1, 2], 'b': ['hello', 'hello']}
    """
    y = {}
    keys = None
    for i, z in enumerate(x):
        if keys is None:
            keys = set(z)
        elif keys != set(z):
            raise ValueError(
                f"Iterable has inconsistent keys at position {i}: expected {keys}, got "
                f"{set(keys)}."
            )
        for key, value in z.items():
            y.setdefault(key, []).append(value)
    return y


def transpose_to_list(x: Mapping[Any, Iterable]) -> List[Dict]:
    """
    Transpose a mapping of iterables to a list of dictionaries.
    """
    sizes = {key: len(value) for key, value in x.items()}
    unique_sizes = set(sizes.values())
    if len(unique_sizes) > 1:
        raise ValueError(f"Mapping has inconsistent sizes: {sizes}.")
    (size,) = unique_sizes
    y = []
    for i in range(size):
        y.append({key: value[i] for key, value in x.items()})
    return y


def _update_or_union(
    inplace: bool, x: dict, y: Optional[Mapping] = None, **kwargs
) -> dict:
    if not inplace:
        x = dict(x)
    y = y or {}
    y.update(kwargs)

    for key, value in y.items():
        if value is Delete:
            x.pop(key)
        else:
            x[key] = value

    return x


def union(x, y: Optional[Mapping] = None, **kwargs):
    """
    Union of two dictionaries, yielding a new instance.

    Args:
        x: Dictionary to update.
        y: Values to update as a mapping (may contain :class:`Delete` to delete a
            value).
        **kwargs: Values to update as keyword arguments (may contain :class:`Delete` to
            delete a value).

    Returns:
        Union of the dictionaries.

    Examples:

        >>> from collectiontools import Delete, union
        >>>
        >>> x = {"a": 3, "b": 9}
        >>> union(x, {"c": "hello"}, a=Delete)
        {'b': 9, 'c': 'hello'}
        >>> "a" in x
        True
    """
    return _update_or_union(False, x, y, **kwargs)


def update(x: dict, y: Optional[Mapping] = None, **kwargs):
    """
    Update a dictionary in-place.

    Args:
        x: Dictionary to update.
        y: Values to update as a mapping (may contain :class:`Delete` to delete a
            value).
        **kwargs: Values to update as keyword arguments (may contain :class:`Delete` to
            delete a value).

    Returns:
        Updated dictionary.

    Examples:

        >>> from collectiontools import Delete, update
        >>>
        >>> x = {"a": 3, "b": 9}
        >>> update(x, {"c": "hello"}, a=Delete)
        {'b': 9, 'c': 'hello'}
        >>> "a" in x
        False
    """
    return _update_or_union(True, x, y, **kwargs)


class Delete:
    """
    Delete an object.

    .. seealso::

        :func:`union` and :func:`update` delete keys from a dictionary if the
        corresponding value is :class:`Delete`.
    """
