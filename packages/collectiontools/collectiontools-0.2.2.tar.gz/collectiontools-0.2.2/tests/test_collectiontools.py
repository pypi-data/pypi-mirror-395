import collectiontools as ct
import pytest


def test_transpose() -> None:
    x = [
        {"a": 1, "b": {1, 2}},
        {"a": "foo", "b": None},
    ]
    y = {
        "a": [1, "foo"],
        "b": [{1, 2}, None],
    }
    assert ct.transpose_to_dict(x) == y
    assert ct.transpose_to_list(y) == x
    assert ct.transpose(x) == y
    assert ct.transpose(y) == x
    assert ct.transpose(ct.transpose(x)) == x
    assert ct.transpose(ct.transpose(y)) == y

    with pytest.raises(ValueError, match="inconsistent keys"):
        ct.transpose_to_dict(
            [
                {"a": 1, "b": {1, 2}},
                {"a": "foo"},
            ]
        )

    with pytest.raises(ValueError, match="inconsistent sizes"):
        ct.transpose_to_list(
            {
                "a": [],
                "b": [1],
            }
        )

    with pytest.raises(ValueError, match="mapping or iterable"):
        ct.transpose(7)


def test_map_values():
    assert ct.map_values(lambda x: 2 * x, {"a": 1, "b": "hello"}) == {
        "a": 2,
        "b": "hellohello",
    }
    assert ct.map_values(
        lambda x: 2 * x, {"a": 1, "b": {"c": "hello"}}, recursive=True
    ) == {
        "a": 2,
        "b": {"c": "hellohello"},
    }


def test_update_and_union():
    x = {"a": "b", "c": 1}
    assert ct.update(x, {"a": ct.Delete, "c": 7, "d": None}) == {"c": 7, "d": None}
    assert "a" not in x
    assert ct.union(x, d=ct.Delete, c=9) == {"c": 9}
    assert "d" in x


def test_filter_values():
    assert ct.filter_values(
        lambda x: isinstance(x, int), {"a": 1, "b": 2, "c": "hello"}
    ) == {"a": 1, "b": 2}


def test_append_values():
    x = {}
    assert ct.append_values(x, {"a": 1, "b": "c"}) == {"a": [1], "b": ["c"]}
    assert ct.append_values(x, {"a": 2, "b": "d"}) == {"a": [1, 2], "b": ["c", "d"]}
