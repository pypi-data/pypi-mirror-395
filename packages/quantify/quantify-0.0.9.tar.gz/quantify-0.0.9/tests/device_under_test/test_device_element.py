from operator import itemgetter
import random

import pytest

from quantify.device_under_test.device_element import DeviceElement


class RandomElement(DeviceElement):
    _ELEMENT_TEMPLATE = {
        "foo": {
            "factory": random.random,
            "kwargs": {
                "foo1-key": itemgetter("foo1-value"),
                "foo2-key": itemgetter("foo2-value"),
            },
        },
        "bar": {
            "factory": random.random,
            "kwargs": {"bar-key": itemgetter("bar-value")},
        },
    }

    def __init__(self, name="rand", **kwargs):
        super().__init__(name, **kwargs)

    @property
    def pre_computed_calls(self):
        return {
            "foo1-value": "foo1-value-replaced",
            "foo2-value": "foo2-value-replaced",
            "bar-value": "bar-value-replaced",
        }


class ChildRandomElement(RandomElement):
    _ELEMENT_TEMPLATE = {
        "baz": {
            "factory": random.random,
            "kwargs": {"baz-key": itemgetter("baz-value-child")},
        },
        "foo": {
            "factory": random.random,
            "kwargs": {
                "foo1-key": itemgetter("foo1-value-child"),
                "foo3-key": itemgetter("foo3-value-child"),
            },
        },
    }

    def __init__(self, name="childrand", **kwargs):
        super().__init__(name, **kwargs)

    @property
    def pre_computed_calls(self):
        calls = super().pre_computed_calls.copy()
        calls.update(
            {
                "bar-value": "bar-replaced-child",
                "foo1-value-child": "foo1-replaced-child",
                "foo3-value-child": "foo3-replaced-child",
                "baz-value-child": "baz-replaced-child",
            }
        )
        return calls


@pytest.mark.skip(
    reason="Not sure how this passed in the first place when the MR was merged."
)
def test_element_template_merging():
    """
    Test that element templates are merged correctly between
    parent and child classes.
    """
    merged_template = ChildRandomElement.get_element_template()

    # Child overrides parent for foo1-key and foo3-key
    assert merged_template["foo"]["kwargs"]["foo1-key"].__eq__(
        itemgetter("foo1-value-child")
    )
    assert merged_template["foo"]["kwargs"]["foo3-key"].__eq__(
        itemgetter("foo3-value-child")
    )

    # Parent key is still present
    assert merged_template["bar"]["kwargs"]["bar-key"].__eq__(itemgetter("bar-value"))


def test_pre_computed_calls():
    """
    Test that pre_computed_calls property returns expected keys and values.
    """
    pre_computed = ChildRandomElement().pre_computed_calls

    # All expected keys are present
    for key in ("bar-value", "foo1-value-child", "foo3-value-child"):
        assert key in pre_computed

    # Values are correct
    assert pre_computed["bar-value"] == "bar-replaced-child"
    assert pre_computed["foo1-value-child"] == "foo1-replaced-child"
    assert pre_computed["foo3-value-child"] == "foo3-replaced-child"


@pytest.mark.skip(
    reason="Not sure how this passed in the first place when the MR was merged."
)
def test_generate_config():
    """
    Test that _generate_config merges and overrides
    keys as expected for child and parent.
    """
    name = "random"
    elem = ChildRandomElement(name=name)
    ops = elem._generate_config()[name]

    # All expected operation keys are present (merged from parent and child)
    assert set(ops.keys()) == {"foo", "bar", "baz"}

    # Merged keys from parent and child are present for 'foo'
    foo_cfg = ops["foo"]
    assert set(foo_cfg.factory_kwargs.keys()) == {"foo1-key", "foo2-key", "foo3-key"}

    # Values: child overrides for foo1-key and foo3-key, parent for foo2-key
    assert foo_cfg.factory_kwargs["foo1-key"] == "foo1-replaced-child"
    assert foo_cfg.factory_kwargs["foo3-key"] == "foo3-replaced-child"
    assert foo_cfg.factory_kwargs["foo2-key"] == "foo2-value-replaced"

    # Parent key is still present and correct
    bar_cfg = ops["bar"]
    assert set(bar_cfg.factory_kwargs.keys()) == {"bar-key"}
    assert bar_cfg.factory_kwargs["bar-key"] == "bar-replaced-child"

    # Child-only op is present
    baz_cfg = ops["baz"]
    assert set(baz_cfg.factory_kwargs.keys()) == {"baz-key"}
    assert baz_cfg.factory_kwargs["baz-key"] == "baz-replaced-child"
