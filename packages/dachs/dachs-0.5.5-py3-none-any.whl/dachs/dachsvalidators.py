import logging

from dachs import ureg


def isQuantity(instance, attribute, value):
    assert isinstance(value, ureg.Quantity), logging.error(
        f"{attribute=} should be specified as a quantity with a unit"
    )
