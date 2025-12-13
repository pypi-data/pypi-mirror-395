import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

from dachs import ureg
from dachs.equipment import PV, Equipment
from dachs.metaclasses import Experiment, ExperimentalSetupClass
from dachs.readers import ReadStartingCompounds, readRawMessageLog
from dachs.reagent import Chemical, Mixture, Product, Reagent
from dachs.synthesis import RawLogMessage


def test_equipment() -> None:
    """Just a basic test of the class"""
    solvent = Equipment(
        ID="BATH_1",
        EquipmentName="Lauda Bath",
        Manufacturer="Lauda",
        ModelName="Proline Edition X RP 855 C Cooling thermostat 230 V; 50 Hz",
        ModelNumber="L001603",
        UnitPrice=ureg.Quantity("9756 euro"),
        UnitSize=ureg.Quantity("1 item"),
        Description="funky bath with excellent temperature control",
        PVs={
            "temp": PV(
                ID="temp",
                PVName="temperature",
                Description="Setpoint temperature of the bath",
                CalibrationFactor=1.0,
                CalibrationOffset="0 kelvin",
                Setpoint="20 kelvin",  # can also be set at a later stage, just wanted to check the units.
            )
        },
    )
    e2 = Equipment(
        ID="VESS_1",
        EquipmentName="Falcon tube",
        Manufacturer="Labsolute",
        ModelName="Centrifuge Tube 50 ml, PP",
        ModelNumber="7696884",
        UnitPrice=ureg.Quantity("202 euro"),
        UnitSize=ureg.Quantity("300 items"),
        Description="Falcon tubes, 50 ml",
        PVs={},
    )
    assert list(solvent.keys()) == [
        'ID', 'EquipmentID', 'EquipmentName', 'Manufacturer', 'ModelName', 'ModelNumber', 'Description',
        'PriceDate', 'UnitPrice', 'UnitSize', 'PVs', '_excludeKeys', '_storeKeys', '_loadKeys']
    assert solvent._loadKeys == ['ID', 'EquipmentID', 'EquipmentName', 'Manufacturer', 'ModelName',
                                 'ModelNumber', 'Description', 'PriceDate', 'UnitPrice', 'UnitSize', 'PVs']
    ppu = e2.PricePerUnit()
    assert ppu.u == "EUR"
    assert ppu.m == pytest.approx(.6733333)


def test_readEquipment() -> None:
    filename = Path("tests", "testData", "AutoMOFs_The_Logbook.xlsx")
    SetupName = "AMSET_6"

    # read equipment list:
    eq = pd.read_excel(filename, sheet_name="Equipment", index_col=None, header=0)
    eq = eq.dropna(how="all")
    eqDict = {}
    for rowi, equip in eq.iterrows():
        try:
            eqItem = Equipment(
                ID=str(equip["Equipment ID"]),
                EquipmentName=str(equip["Equipment Name"]),
                Manufacturer=str(equip["Manufacturer"]),
                ModelName=str(equip["Model Name"]),
                ModelNumber=str(equip["Model Number"]),
                UnitPrice=ureg.Quantity(str(equip["Unit Price"]) + " " + str(equip["Price Unit"])),
                UnitSize=ureg.Quantity(str(equip["Unit Size"]) + " " + str(equip["Unit"])),
                Description=str(equip["Description"]),
                PVs={},
            )
            eqDict.update({str(equip["Equipment ID"]): eqItem})
        except Exception as e:
            import traceback
            traceback.print_exception(e)
            print(f'Failure reading {equip["Equipment ID"]=}\n {str(e)}')

    # read setup configuration:
    df = pd.read_excel(filename, sheet_name="Setup", index_col=None, header=0)
    df = df.dropna(how="all")
    dfRow = df.loc[df.SetupID == SetupName].copy()
    assert len(dfRow == 1), f"More or less than one entry found for {SetupName=} in {filename=}"
    # get all equipment for the setup
    itemList = [dfRow[i].item() for i in dfRow.keys() if "ID_" in i]
    eqList = [eqDict[item] for item in itemList if item in eqDict.keys()]
    _ = ExperimentalSetupClass(
        ID=dfRow["SetupID"],
        SetupName=dfRow["Name"],
        Description=dfRow["Description"],
        EquipmentList=eqList,
    )
    assert filename == Path("tests/testData/AutoMOFs_The_Logbook.xlsx")


def test_experiment() -> None:
    ex = Experiment(
        ID="AutoMOF5",
        ExperimentName="Automatic MOF Exploration series 5",
        Description="""
            In this series, MOFs are synthesised in methanol from two stock solutions,
            all performed at room temperature (see environmental details in log).
            The injection rate and injection order are varied. Centrifugation and drying
            is performed manually. Residence times are 20 minutes after start of second injection.
        """,)
    assert list(ex.keys()) == ['ID', 'ExperimentName', 'Description', 'Chemicals', 'Synthesis',
                               'ExperimentalSetup', '_excludeKeys', '_storeKeys', '_loadKeys']


def test_experimental_setup() -> None:
    """Just a basic test of the class"""
    eq1 = Equipment(
        ID="BATH_1",
        EquipmentName="Lauda Bath",
        Manufacturer="Lauda",
        ModelName="Proline Edition X RP 855 C Cooling thermostat 230 V; 50 Hz",
        ModelNumber="L001603",
        UnitPrice=ureg.Quantity("9756 euro"),
        UnitSize=ureg.Quantity("1 item"),
        Description="funky bath with excellent temperature control",
    )

    su1 = ExperimentalSetupClass(
        ID="AMSET_6",
        SetupName="AutoMof Configuration 6",
        Description="Same as AMSET_4 but Rod shaped stirring bar",
        EquipmentList=[eq1],
    )
    assert list(su1.keys()) == ['ID', 'ExperimentalSetupID', 'SetupName', 'Description', 'EquipmentList',
                                '_excludeKeys', '_storeKeys', '_loadKeys']
    assert list(eq1.keys()) == ['ID', 'EquipmentID', 'EquipmentName', 'Manufacturer', 'ModelName', 'ModelNumber',
                                'Description', 'PriceDate', 'UnitPrice', 'UnitSize', 'PVs', '_excludeKeys',
                                '_storeKeys', '_loadKeys']
    assert su1.EquipmentList[0] == eq1


def test_readRawMessageLog() -> None:
    filename = Path("tests", "testData", "log_AutoMOFs_6_L019.xlsx")
    logs = readRawMessageLog(filename)
    assert len(logs) == 25
    assert all([isinstance(log, RawLogMessage) for log in logs])


def test_ReadStartingCompounds() -> None:
    filename = Path("tests", "testData", "AutoMOFs_The_Logbook.xlsx")
    comp = ReadStartingCompounds(filename)
    assert len(comp) == 22
    assert all([isinstance(c, Reagent) for c in comp])


def test_product() -> None:
    # define a zif Chemical:
    zifChemical = Chemical(
        ID="Zif-8",
        ChemicalName="Zif-8",
        ChemicalFormula="ZnSomething",
        MolarMass=ureg.Quantity("229 g/mol"),
        Density=ureg.Quantity("0.335 g/cc"),
        SourceDOI="something",
    )
    prod = Product(ID="ZIF-8", Chemical=zifChemical, Mass=ureg.Quantity("12.5 mg"), Purity="99 percent")
    assert list(prod.keys()) == ['ID', 'Chemical', 'Mass', 'Purity', 'Evidence', '_excludeKeys',
                                 '_storeKeys', '_loadKeys']
    assert prod.Chemical.MolarMass.m == 229


def test_reagent() -> None:
    """
    Tests for the Reagent class
    """
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    solvent = Reagent(
        ID="Solvent_1",
        Chemical=Chemical(
            ID="MeOH",
            ChemicalName="Methanol",
            ChemicalFormula="CH3OH",
            MolarMass=ureg.Quantity("32.04 g/mol"),
            Density=ureg.Quantity("0.79 g/ml"),
        ),
        CASNumber="67-56-1",
        Brand="Chemsolute",
        UNNumber="1230",
        MinimumPurity="98 percent",
        OpenDate="2022-05-01T10:04:22",
        StorageConditions=None,
        UnitPrice="9 euro",
        UnitSize="2.5 liter",
    )
    linker = Reagent(
        ID="linker_1",
        Chemical=Chemical(
            ID="2-MIM",
            ChemicalName="2-methylimidazole",
            ChemicalFormula="C4H6N2",
            MolarMass=ureg.Quantity("82.11 g/mol"),
            Density=ureg.Quantity("1.096 g/ml"),
        ),
        CASNumber="693-98-1",
        Brand="Sigma-Aldrich",
        UNNumber="3259",
        MinimumPurity="99 percent",
        OpenDate="2019-05-01T10:04:22",
        StorageConditions="air-conditioned lab",
        UnitPrice="149 euro",
        UnitSize="1000 gram",
    )
    assert solvent._loadKeys == ['ID', 'Chemical', 'CASNumber', 'Brand', 'UNNumber', 'MinimumPurity',
                                 'OpenDate', 'StorageConditions', 'UnitPrice', 'UnitSize', 'Used']
    price = ureg("12.4 percent") * solvent.UnitPrice
    assert price.m == 1.116
    assert price.u == "EUR"
    ppu = solvent.PricePerUnit()
    assert ppu.m == 3.6
    assert ppu.u == "EUR / liter"

    # make mixture:
    mixture = Mixture(
        ID="stock_1",
        MixtureName="linker stock solution",
        Description="Stock solution of linker at 78 g/mole",
        PreparationDate=pd.to_datetime("2022.07.27"),
        StorageConditions="air conditioned lab",
        ComponentList=[solvent, linker],
        ComponentMasses={
            solvent.ID: ureg.Quantity("4.5767 g"),
            linker.ID: solvent.MassByVolume(ureg.Quantity("500 ml")),
        },
    )
    msg = [f"{c.MolesByMass(mixture.ComponentMasses[c.ID]):.3f} of {c.Chemical.ChemicalName} in"
           f" {mixture.MixtureName} at mole concentration"
           f" {mixture.component_concentration(MatchComponent=c):0.03e}"
           for ci, c in enumerate(mixture.ComponentList)]
    assert msg[0] == (
        "0.143 mole of Methanol in linker stock solution at mole concentration 2.884e-02 dimensionless")
    assert msg[1] == (
        "4.811 mole of 2-methylimidazole in linker stock solution at mole concentration 9.712e-01 dimensionless")
    logging.info(msg)
    msg = [f"{c.price_per_mass():.3f} of {c.Chemical.ChemicalName} in {mixture.MixtureName}"
           for c in mixture.ComponentList]
    assert msg[0] == "0.005 EUR / gram of Methanol in linker stock solution"
    assert msg[1] == "0.149 EUR / gram of 2-methylimidazole in linker stock solution"
    logging.info(msg)
    mc = mixture.component_concentrations()
    assert len(mc) == 2
    assert mc[0].m == pytest.approx(0.028837061)
    assert mc[1].m == pytest.approx(0.971162939)
    assert all([str(q.u) == "dimensionless" for q in mc])
    assert mixture.total_mass.m == pytest.approx(399.5767)
    assert mixture.total_mass.u == "gram"
    assert mixture.total_price.m == pytest.approx(58.87585584)
    assert mixture.total_price.u == "EUR"
    logging.info(f"\n {mixture.component_concentrations()=}, {mixture.total_mass=}, {mixture.total_price=}")
