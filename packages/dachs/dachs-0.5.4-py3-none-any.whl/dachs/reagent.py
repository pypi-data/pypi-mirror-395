#!/usr/bin/env python
# coding: utf-8

"""
A dataclass for specifying a Reagent, Reagentmixture or Product.
"""
from __future__ import annotations

import chempy
from pandas import Timestamp

from dachs.equipment import Equipment
from dachs.helpers import whitespaceCleanup

# from dachs.metaclasses import EnvironmentClass # to get around using Mixture typing inside the Mixture class

__author__ = "Brian R. Pauw"
__contact__ = "brian@stack.nl"
__license__ = "GPLv3+"
__date__ = "2022/11/07"
__status__ = "beta"


import logging
from typing import Dict, List, Optional, Union

from attrs import Factory, define, field, validators

from dachs import ureg  # get importError when using: "from . import ureg"
from dachs.additemstoattrs import addItemsToAttrs
from dachs.synthesis import SynthesisClass

# from dachsvalidators import isQuantity


@define
class Chemical(addItemsToAttrs):
    """Base chemistry which underpins both Reagents and Products"""

    ID: str = field(
        default="Chemical",
        validator=validators.instance_of(str),
        converter=str,
    )
    ChemicalName: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    ChemicalFormula: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    ChemicalID: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    MolarMass: Optional[ureg.Quantity] = field(
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
        # converter=ureg,
    )
    Density: Optional[ureg.Quantity] = field(
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
        # converter=ureg,
    )
    Substance: Optional[chempy.Substance] = field(
        default=None,
        validator=validators.optional(validators.instance_of(chempy.Substance)),
        # converter=chempy.Substance.from_formula,
    )
    SourceDOI: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    SpaceGroup: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    # internals, don't need a lot of validation:
    _excludeKeys: list = ["_excludeKeys", "_storeKeys", "Substance"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing


@define
class Product(addItemsToAttrs):
    """
    Defines a chemical Product as having a chemical structure, with a target mass (100% conversion)
    and an actual mass.
    """

    ID: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    Chemical: Chemical = field(
        default=None,
        validator=validators.instance_of(Chemical),
        # converter=Reagent,
    )
    Mass: Optional[ureg.Quantity] = field(
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
        # converter=ureg,
    )
    Purity: Optional[float] = field(
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
        converter=ureg,
    )
    Evidence: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
        converter=str,
    )
    _excludeKeys: list = [
        "_excludeKeys",
        "_storeKeys",
        "SynthesisYield",
    ]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing

    # def SynthesisYield(self):
    #     assert (self.ActualMass is not None) and (
    #         self.TargetMass is not None
    #     ), logging.warning(
    #         "Yied can only be calculated when both target mass and actual mass are set"
    #     )
    #     assert self.TargetMass > self.Mass, logging.warning(
    #         "target mass has to be bigger than actual mass"
    #     )
    #     return self.Mass / self.TargetMass


@define
class Reagent(addItemsToAttrs):
    ID: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    Chemical: Chemical = field(
        default=None,
        validator=validators.instance_of(Chemical),
        # converter=Reagent,
    )
    # Name and the following are in Chemical
    CASNumber: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    Brand: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    UNNumber: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    MinimumPurity: float = field(
        default=None,
        validator=validators.instance_of(ureg.Quantity),
        converter=ureg,
    )
    OpenDate: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    StorageConditions: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
        converter=str,
    )
    UnitPrice: Optional[float] = field(
        default=None,
        validator=validators.instance_of(ureg.Quantity),
        converter=ureg,
    )
    UnitSize: float = field(
        default=None,
        validator=validators.instance_of(ureg.Quantity),
        converter=ureg,
    )
    Used: bool = field(
        default=False,
        validator=validators.instance_of(bool),
        converter=bool,
    )
    # internals, don't need a lot of validation:
    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing

    def _CheckForDensity(self):
        assert self.Chemical.Density is not None, logging.warning("Chemical.Density must be provided")
        return

    def _CheckForMolarMass(self):
        assert self.Chemical.MolarMass is not None, logging.warning("Chemical.MolarMass must be provided")
        return

    # @property
    def _CheckForPriceCalc(self):
        self._CheckForDensity()
        assert (self.UnitPrice is not None) and (self.UnitSize is not None), logging.warning(
            "Price calculations can only be done when UnitSize and UnitPrice as well as Chemical.Density are set"
        )
        return

    # @property
    def PricePerUnit(self) -> ureg.Quantity:
        self._CheckForPriceCalc()
        return self.UnitPrice / self.UnitSize

    # @property
    def price_per_mass(self) -> Union[ureg.Quantity, None]:
        self._CheckForPriceCalc()
        if self.UnitSize.check("[mass]"):
            return self.PricePerUnit()
        elif self.UnitSize.check("[volume]"):
            return (self.PricePerUnit() / self.Chemical.Density).to("euro/g")
        else:
            logging.warning(f"Price per mass cannot be calculated from {self.PricePerUnit=}")
            return None

    # @property
    def PricePerMole(self) -> ureg.Quantity:
        self._CheckForMolarMass()
        assert (
            self.price_per_mass() is not None
        ), "Price per mole cannot be calculated as price per mass cannot be calculated"
        return (self.price_per_mass() * self.Chemical.MolarMass).to("euro/mole")

    def MolesByMass(self, mass: ureg.Quantity) -> ureg.Quantity:
        self._CheckForDensity()
        self._CheckForMolarMass()
        mass.check("[mass]")
        return (mass / self.Chemical.MolarMass).to("mole")

    def MassByVolume(self, volume: ureg.Quantity) -> ureg.Quantity:
        self._CheckForDensity()
        volume.check("[volume]")
        return (volume * self.Chemical.Density).to("gram")


@define
class Mixture(addItemsToAttrs):
    """This class supersedes the ReagentMixture class, and allows Mixtures of Reagents as well as Mixtures of
    Mixtures."""

    ID: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    MixtureName: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=str,
    )
    Description: str = field(
        default=None,
        validator=validators.instance_of(str),
        converter=whitespaceCleanup,
    )
    DetailedDescription: str = field(
        default="",
        validator=validators.instance_of(str),
        converter=str,
    )
    ComponentList: List[Union[Reagent, None]] = (
        field(  # list of Reagents, there is a method to add Mixtures (as individual reagents)
            default=Factory(list),
            validator=validators.instance_of(list),
        )
    )
    ComponentMasses: Dict[str, Union[ureg.Quantity, None]] = field(  # masses of the aforementioned components.
        default=Factory(dict),
        validator=validators.instance_of(dict),
    )
    PreparationDate: Timestamp = field(default=None, validator=validators.instance_of(Timestamp))
    # str = field(
    #     default=None,
    #     validator=validators.instance_of(str),
    #     converter=str,
    # )
    Density: Optional[ureg.Quantity] = field(  # can be (re)defined for each mixture. cannot be calculated.
        default=None,
        validator=validators.optional(validators.instance_of(ureg.Quantity)),
        # converter=ureg,
    )
    StorageConditions: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
        converter=str,
    )
    Synthesis: Optional[SynthesisClass] = field(
        default=None,
        validator=validators.optional(validators.instance_of(SynthesisClass)),
    )
    # Environment: Optional[EnvironmentClass] = field(
    #     default=None,
    #     validator=validators.optional(validators.instance_of(EnvironmentClass)),
    # )
    Container: Optional[Equipment] = field(
        default=None,
        validator=validators.optional(validators.instance_of(Equipment)),
    )
    # internals, don't need a lot of validation:
    _excludeKeys: list = ["_excludeKeys", "_storeKeys"]  # exclude from HDF storage
    _storeKeys: list = []  # store these keys (will be filled in later)
    _loadKeys: list = []  # load these keys from file if reconstructing

    def component_concentrations(self) -> List[ureg.Quantity]:
        # returns a list of mole concentrations of the Reagents
        return [self.component_concentration(MatchComponent=i).to("mole/mole") for i in self.ComponentList]

    def add_reagent_to_mix(self, reag: Reagent, ReagentMass: ureg.Quantity) -> None:
        """Adds a reagent to the mixture"""
        if reag not in self.ComponentList:
            self.ComponentList += [reag]
            self.ComponentMasses[reag.ID] = ReagentMass
        else:
            self.ComponentMasses[reag.ID] += ReagentMass

        self.DetailedDescription += f"{ReagentMass:.2f~P} of {reag.Chemical.ChemicalName}, and "
        # mark the reagent as actually in use:
        reag.Used = True
        return

    def add_mixture_to_mix(
        self,
        mix: Mixture,
        AddMixtureMass: ureg.Quantity = None,
        AddMixtureVolume: ureg.Quantity = None,
        MixtureDensity: ureg.Quantity = None,
    ) -> None:
        """Adds a mixture to this Mixture"""
        # First we find out what fraction of the total mixture mass we are taking on board
        # if we are supplied with volume and density, we convert to mass first:
        if AddMixtureMass is None:
            assert (AddMixtureVolume is not None) and (
                MixtureDensity is not None
            ), "If added mixture mass is not supplied, both volume and density must be defined"
            assert AddMixtureVolume.check("[volume]"), "AddMixtureVolume must be a volume"
            assert MixtureDensity.check("[mass]/[volume]"), "MixtureDensity must be a density (mass per volume)"
            AddMixtureMass = AddMixtureVolume * MixtureDensity
        # Check that we are making sense
        assert (
            AddMixtureMass <= mix.total_mass
        ), "Sanity check failed, you are adding more mass of mixture than existed in the mixture."
        MassFractionOfTotal = (AddMixtureMass / mix.total_mass).to("gram/gram")
        for ci, component in enumerate(mix.ComponentList):
            if component not in self.ComponentList:
                self.ComponentList += [component]
                self.ComponentMasses[component.ID] = mix.ComponentMasses[component.ID] * MassFractionOfTotal
            else:
                self.ComponentMasses[component.ID] += mix.ComponentMasses[component.ID] * MassFractionOfTotal

        if AddMixtureVolume is not None:
            self.DetailedDescription += (
                f"{AddMixtureVolume:.2f~P} ({AddMixtureMass:.2f~P} when assuming a density of"
                f" {MixtureDensity:.2f~P}) of {mix.Description}, and "
            )
        else:
            self.DetailedDescription += f"{AddMixtureMass} of {mix.Description}, and "

        return

    def component_moles(self, MatchComponent: Reagent) -> ureg.Quantity:
        componentMoles = 0
        for ci, component in enumerate(self.ComponentList):
            theseMoles = component.MolesByMass(self.ComponentMasses[component.ID])
            if component == MatchComponent:
                componentMoles += theseMoles
        if componentMoles == 0:
            logging.warning(f"Concentration of {MatchComponent=} is zero, component not found")
        return componentMoles

    def total_moles(self) -> ureg.Quantity:
        totalMoles = 0
        for ci, component in enumerate(self.ComponentList):
            theseMoles = component.MolesByMass(self.ComponentMasses[component.ID])
            totalMoles += theseMoles
        return totalMoles

    def component_concentration(self, MatchComponent: Reagent) -> float:
        """
        Finds the concentration of a component defined by its entry in the total mixture
        This concentration will be in mole fraction.
        """
        return self.component_moles(MatchComponent) / self.total_moles()

    @property
    def total_mass(self) -> ureg.Quantity:
        # returns the total mass of the mixture
        TMass = ureg.Quantity("0 gram")
        for mass in self.ComponentMasses.values():
            TMass += mass
        return TMass

    @property
    def total_price(self) -> ureg.Quantity:
        # returns the total cost of the miture
        # assert False, 'Price calculation Not implemented yet.'
        TPrice = 0
        for ci, component in enumerate(self.ComponentList):
            TPrice += component.price_per_mass() * self.ComponentMasses[component.ID]
        return TPrice

    def price_per_mass(self) -> ureg.Quantity:
        # assert False, 'Price calculation Not implemented yet.'
        # returns the cost per mass of the mixture
        return self.total_price / self.total_mass
