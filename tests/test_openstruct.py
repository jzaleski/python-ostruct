import pytest
from ostruct import OpenStruct


def test_empty_struct():
    o = OpenStruct()

    assert o == {}
    assert isinstance(o, OpenStruct)
    assert isinstance(o.__dict__, dict)

    if o:
        assert False
    else:
        assert True

    if not o:
        assert True
    else:
        assert False


def test_shallow_struct():
    o = OpenStruct()
    o.a = 10

    assert o.a == 10

    if o:
        assert True
    else:
        assert False

    if not o:
        assert False
    else:
        assert True


def test_nested_struct():
    o = OpenStruct()
    o.a.b.c.d = 10

    assert o.a.b.c.d == 10
    assert o.a.b.c == {'d': 10}
    assert o.a.b == {'c': {'d': 10}}
    assert o.a == {'b': {'c': {'d': 10}}}
    assert o == {'a': {'b': {'c': {'d': 10}}}}


def test_constructor_clone():
    o = OpenStruct(a=1, b=2, c=4)
    assert o == {'a': 1, 'b': 2, 'c': 4}

    a = OpenStruct(o)
    assert o == a

    b = OpenStruct(o.__dict__)
    assert o == b

    c = OpenStruct(**(o.__dict__))
    assert o == c

    d = OpenStruct(**o)
    assert o == d


@pytest.mark.parametrize("value,expected", [
    (1, 1),
    ('Hello', 'Hello'),
    ((), ()),
    ((1, 2), (1, 2)),
    (('Hello', 'World'), ('Hello', 'World')),
    ([], []),
    ([1, 2], [1, 2]),
    (['Hello', 'World'], ['Hello', 'World']),
    ({'a': 1, 'b': 2}, OpenStruct({'a': 1, 'b': 2})),
    (({'a': 1, 'b': 2}, {'c': 3}), ({'a': 1, 'b': 2}, {'c': 3})),
    ([{'a': 1, 'b': 2}, {'c': 3}], [{'a': 1, 'b': 2}, {'c': 3}]),
    (OpenStruct({'a': 1, 'b': 2}), OpenStruct({'a': 1, 'b': 2})),
    ((OpenStruct({'a': 1, 'b': 2})), (OpenStruct({'a': 1, 'b': 2}))),
    ([OpenStruct({'a': 1, 'b': 2})], [OpenStruct({'a': 1, 'b': 2})]),
])
def test_convert(value, expected):
    assert OpenStruct._convert(value) == expected


@pytest.mark.parametrize("value", [
    1,
    1.2,
    (1, 2, 3),
    [{'a': 1, 'b': 2, 'c': 4}],
    'Hello',
    lambda x: x**2
])
def test_constructor_bad_args(value):
    with pytest.raises(TypeError):
        OpenStruct(value)


def test_comparisons():
    o1 = OpenStruct()
    o1.a.b.c = 10

    assert (o1 == 10) is False
    assert (o1 is True) is False

    o2 = OpenStruct()
    o2.a.b.c = 10

    assert (o1 == o2) is True
    assert (o1 != o2) is False
    assert (o1 is o2) is False
    assert (o2 is o1) is False

    with pytest.raises(TypeError):
        o1 > o2

    with pytest.raises(TypeError):
        o1 < o2

    with pytest.raises(TypeError):
        o1 >= o2

    with pytest.raises(TypeError):
        o1 <= o2


def test_iteritems():
    s = 0
    o = OpenStruct()

    o.a = 1
    o.b = 2
    o.c = 4
    o.d = 8

    for key, value in o.iteritems():
        s += value

    assert s == 15


def test_items():
    s = 0
    o = OpenStruct()

    o.a = 1
    o.b = 2
    o.c = 4
    o.d = 8

    for key, value in o.items():
        s += value

    assert s == 15


def test_keys():
    o = OpenStruct()
    assert len(o.keys()) == 0

    o = OpenStruct(a=1, b=2, c=4)
    assert sorted(o.keys()) == sorted(['a', 'b', 'c'])


def test_set_get_item():
    o = OpenStruct()
    o['a'] = 10
    assert o['a'] == 10
    assert o.a == 10

    o = OpenStruct()
    o['a']['b']['c'] = 10
    assert o['a']['b']['c'] == 10
    assert o['a']['b'] == {'c': 10}
    assert o['a'] == {'b': {'c': 10}}
    assert o == {'a': {'b': {'c': 10}}}


def test_delete_item():
    o = OpenStruct(a=1, b=2, c=4)

    del o.b
    assert o == {'a': 1, 'c': 4}

    o.b.d.e = 10

    del o.b.d
    assert o == {'a': 1, 'c': 4, 'b': {}}

    del o
    with pytest.raises(NameError):
        assert o  # NoQA


@pytest.mark.parametrize("value,expected", [
    (None, 0),
    ({'a': 1, 'b': 2, 'c': 4}, 3),
    (OpenStruct(a=1, b=2, c=4, d=8), 4),
])
def test_len(value, expected):
    o = OpenStruct(value)
    assert len(o) == expected
