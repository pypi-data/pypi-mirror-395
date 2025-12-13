#!/usr/bin/env python
# coding: utf-8

"""
A dataclass for describing a synthesis
"""

__author__ = "Brian R. Pauw"
__contact__ = "brian@stack.nl"
__license__ = "GPLv3+"
__date__ = "2022/11/07"
__status__ = "beta"

from typing import List, Optional, Union

import chempy
import pint
import yaml
from attrs import Factory, converters, define, field, validators
from pandas import Timestamp

from dachs import ureg  # get importError when using: "from . import ureg"
from dachs.additemstoattrs import addItemsToAttrs
from dachs.equipment import PV
from dachs.helpers import whitespaceCleanup

NoneType = type(None)


def ValConverter(Val):
    """Checks if Val is a string, and if so, converts it to a float or int if possible"""
    if str(Val).strip() != "-":
        return yaml.safe_load(Val) if isinstance(Val, str) else Val
    else:
        return None


def UnitConverter(UnitStr: Union[str, None]) -> Union[str, None]:
    """Checks if UnitStr is a string, and if so, converts it to a string supported by the Pint library"""
    if UnitStr is None:
        return None
    if str(UnitStr).strip() != "-":
        UnitStr = str(UnitStr)
        U = UnitStr.strip()
        U = "percent" if U == "%" else U
        U = "degC" if U == "C" else U
        U = "minute" if U == "mins" else U
        return U
    else:
        return None


def ConvertToQuantity(Val, Unit):
    """Converts a value and unit to a pint/ureg Quantity"""
    condition = 0
    Quantity = None
    # Val, U, Q = None, None, None
    if Val is not None:
        if isinstance(Val, (int, float)):
            condition += 1
    if Unit is not None:
        if (Unit != "-") and (Unit != ""):
            condition += 1
    if condition == 2:  # both value and unit are present
        try:
            Quantity = ureg.Quantity(float(Val), str(Unit))
        except pint.PintError:  # conversion fail
            Quantity = None
    return Quantity


@define
class RawLogMessage(addItemsToAttrs):
    """Attrs-defined class for carrying the raw log messages from the RoWaN synthesis platform"""

    Index: int = field(default=0, validator=validators.instance_of(int))
    TimeStamp: Timestamp = field(default=None, validator=validators.instance_of(Timestamp))
    MessageLevel: str = field(default="", validator=validators.instance_of(str), converter=str)
    ExperimentID: str = field(default="", validator=validators.instance_of(str), converter=str)
    SampleID: str = field(default="", validator=validators.instance_of(str), converter=str)
    Message: str = field(default="", validator=validators.instance_of(str), converter=str)
    Quantity: Optional[ureg.Quantity] = field(
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
    )
    Value: Optional[Union[float, int, str, None]] = field(
        default=None,
        validator=validators.optional(validators.instance_of((int, float, str))),
        converter=converters.optional(ValConverter),
    )
    Unit: Optional[Union[str, None]] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
        converter=converters.optional(UnitConverter),
    )
    Using: Optional[str] = field(default=None, validator=validators.optional(validators.instance_of(str)))
    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.Quantity = ConvertToQuantity(self.Value, self.Unit)


@define
class DerivedParameter(addItemsToAttrs):
    """
    Contains parameters derived from interpretation of the raw log.
    This should link back to the indices of the raw log from which the parameter
    was derived. values can be stored either as pint/ureg Quantities, or as
    Value (float or int) with optional Unit (str) for conversion to Quantities.
    """

    ID: str = field(  # step number
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    ParameterName: str = field(default="", validator=validators.instance_of(str), converter=str)
    Description: str = field(default="", validator=validators.instance_of(str), converter=whitespaceCleanup)
    RawMessages: List[int] = field(
        default=Factory(list),
        validator=validators.instance_of(list),
    )
    Quantity: Optional[ureg.Quantity] = field(
        default=None, validator=validators.instance_of((ureg.Quantity, NoneType))
    )
    Value: Optional[Union[int, float, str]] = field(
        default=None, validator=validators.instance_of((int, float, str, NoneType))
    )
    Unit: str = field(default="", validator=validators.instance_of(str), converter=str)

    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.Quantity = ConvertToQuantity(self.Value, self.Unit)


@define
class synthesisStep(addItemsToAttrs):
    ID: str = field(  # step number
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )

    RawMessage: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    RawMessageLevel: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    TimeStamp: Timestamp = field(default=None, validator=validators.instance_of(Timestamp))
    # str = field(
    #     default=None,
    #     validator=validators.instance_of(str),
    #     converter=str,
    # )
    stepType: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    stepDescription: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=whitespaceCleanup,
    )
    EquipmentId: Optional[str] = field(
        default=Factory(str),
        validator=validators.optional(validators.instance_of(str)),
        # converter=str,
    )
    PVs: Optional[PV] = field(
        default=Factory(PV),
        validator=validators.optional(validators.instance_of(PV)),
        # converter=PV,
    )
    ExperimentId: Optional[str] = field(
        default=Factory(str),
        validator=validators.optional(validators.instance_of(str)),
        # converter=str,
    )
    SampleId: Optional[str] = field(
        default=Factory(str),
        validator=validators.optional(validators.instance_of(str)),
        # converter=str,
    )
    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing


@define
class SynthesisClass(addItemsToAttrs):
    ID: str = field(  # step number
        validator=validators.instance_of(str),
        converter=str,
    )
    Name: str = field(
        validator=validators.instance_of(str),
        converter=str,
    )
    DerivedParameters: List[DerivedParameter] = field(
        default=Factory(list),
        validator=validators.instance_of(list),
    )  # future upgrade to KeyParameters
    Description: Optional[str] = field(  # made optional so it can be added at a later stage...
        default=None,
        validator=validators.optional(validators.instance_of(str)),
        converter=whitespaceCleanup,
    )
    ChemicalReaction: Optional[chempy.Reaction] = field(
        default=None, validator=validators.optional(validators.instance_of(chempy.Reaction))
    )
    RawLog: Optional[List[RawLogMessage]] = field(
        default=None,
        validator=validators.optional(validators.instance_of(list)),
    )
    SynthesisLog: Optional[List[synthesisStep]] = field(
        default=None,
        validator=validators.optional(validators.instance_of(list)),
    )
    SourceDOI: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    KeyParameters: Optional[dict] = field(
        default=Factory(dict),
        validator=validators.optional(validators.instance_of(dict)),
    )
    # DerivedParameters: Optional[List[DerivedParameter]] = field(
    #     default=Factory(list),
    #     validator=validators.optional(validators.instance_of(list)),
    # ) # future upgrade to KeyParameters
    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing
