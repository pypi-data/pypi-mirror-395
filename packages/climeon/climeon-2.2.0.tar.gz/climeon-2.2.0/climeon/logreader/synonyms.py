"""Handling of column names and synonyms."""

# Mapping between correct column names and their synonyms
SYNONYMS = {
    "PowerOutput [kW]": [
        "P_N [kW]",
        "P N [kW]",
        "Power output [kw]",
        "PowerOutput"
    ],
    "NoOfGreasingCyclesFrontBearing [-]": [
        "NoOfGreasingCyclesFrontBearing [kWh]"
    ],
    "NoOfGreasingCyclesRearBearing [-]": [
        "NoOfGreasingCyclesRearBearing [kWh]"
    ],
    "TT0002 [deg C]": [
        "TT02 [deg C]",
        "WHR control temperature [deg C]",
        "WHR control temperature [kW]",
    ],
    "ATU_FlowRatio [-]": [
        "ATU_FlowRatio [l/s]"
    ],
    "ATU_FlowRatioRef [-]": [
        "ATU_FlowRatioRef [l/s]"
    ],
    "ATU_FlowRatioTrigger [-]": [
        "ATU_FlowRatioTrigger [l/s]"
    ],
    "ATU_Trigger [-]": [
        "ATU_Trigger [kW]"
    ],
    "AlertCode [-]": [
        "Alert code [-]"
    ],
    "State [-]": [
        "Module state [-]"
    ],
    "SubState [-]": [
        "Module sub-state [-]"
    ],
    "BoilingPoint [deg C]": [
        "Boiling point [deg C]"
    ],
    "CondensingPoint [deg C]":[
        "Condensing point [deg C]"
    ],
    "InletColdFlow [kg/s]": [
        "Inlet cold Flow [kg/s]",
        "Inlet Cold Flow [kg/s]",
        "Inlet Cold Mass Flow [kg/s]",
    ],
    "InletHotFlow [kg/s]": [
        "Inlet hot Flow [kg/s]",
        "Inlet Hot Flow [kg/s]",
        "Inlet Hot Mass Flow [kg/s]",
    ],
    "InletColdTemp [deg C]": [
        "Inlet cold temp [deg C]"
    ],
    "InletHotTemp [deg C]": [
        "Inlet hot temp [deg C]"
    ],
    "EnthalpyPIDOutput [%]": [
        "Enthalpy PID Output [%]"
    ],
    "ControlMaster [-]": [
        "Control_Master [-]"
    ],
    "MediaFlow [kg/s]": [
        "Media Flow [kg/s]"
    ],
    "CoolingTurbineFlow [kg/s]": [
        "Cooling Turbine Flow [kg/s]"
    ],
    "ThermalPowerTurbine [kW]": [
        "Thermal Power Turbine [kW]"
    ],

    # P1 Deif variables
    "GBState [-]": [
        "GB State [-]"
    ],
    "GenABPhaseAngleL1 [deg]": [
        "GenABPhaseAngle_L1 [deg]"
    ],
    "GenABPhaseAngleL2 [deg]": [
        "GenABPhaseAngle_L2 [deg]"
    ],
    "GenABPhaseAngleL3 [deg]": [
        "GenABPhaseAngle_L3 [deg]"
    ],
    "GenPhaseAngleL1L2 [deg]": [
        "GenPhaseAngle_L1L2 [deg]"
    ],
    "GenPhaseAngleL2L3 [deg]": [
        "GenPhaseAngle_L2L3 [deg]"
    ],
    "GenPhaseAngleL3L1 [deg]": [
        "GenPhaseAngle_L3L1 [deg]"
    ],
    "GenVoltageL1N [V]": [
        "GenVoltage_L1N [V]"
    ],
    "GenVoltageL2N [V]": [
        "GenVoltage_L2N [V]"
    ],
    "GenVoltageL3N [V]": [
        "GenVoltage_L3N [V]"
    ],
    "GenVoltageLLUnbalanced [V]": [
        "GenVoltage_LL_Unbalanced [V]"
    ],
    "GenVoltageLNUnbalanced [V]": [
        "GenVoltage_LN_Unbalanced [V]"
    ],
    "BusPhaseAngleL1L2 [Hz]": [
        "BusPhaseAngle_L1L2 [Hz]"
    ],
    "BusPhaseAngleL2L3 [Hz]": [
        "BusPhaseAngle_L2L3 [Hz]"
    ],
    "BusPhaseAngleL3L1 [Hz]": [
        "BusPhaseAngle_L3L1 [Hz]"
    ],
    "BusVoltageL1L2 [V]": [
        "BusVoltage_L1L2 [V]"
    ],
    "BusVoltageLLUnbalanced [V]": [
        "BusVoltage_LL_Unbalanced [V]"
    ],
    "BusVoltageLNUnbalanced [V]": [
        "BusVoltage_LN_Unbalanced [V]"
    ],

    # Maersk
    "AlertCode1 [-]": [
        "AlertCode1"
    ],
    "AlertCode2 [-]": [
        "AlertCode2"
    ],
    "AlertCode3 [-]": [
        "AlertCode3"
    ],
    "AlertCode4 [-]": [
        "AlertCode4"
    ],
    "AlertCode5 [-]": [
        "AlertCode5"
    ],
    "AV25Pos [%]": [
        "AV25Pos"
    ],
    "EnergyProduced [kWh]": [
        "EnergyProduced"
    ],
    "ExternalColdWaterPumpSpeed [%]": [
        "ExternalColdWaterPumpSpeed"
    ],
    "Fcp91Current [A]": [
        "Fcp91Current"
    ],
    "Fcp91Speed [%]": [
        "Fcp91Speed"
    ],
    "Fcp92Current [A]": [
        "Fcp92Current"
    ],
    "Fcp92Speed [%]": [
        "Fcp92Speed"
    ],
    "FilterPressureDiff [bar]": [
        "FilterPressureDiff"
    ],
    "MainEngineJacketCoolingTemperature [deg C]": [
        "MainEngineJacketCoolingTemperature"
    ],
    "MainEnginePower [kW]": [
        "MainEnginePower"
    ],
    "P101 [bar]": [
        "P101"
    ],
    "P71 [bar]": [
        "P71"
    ],
    "P72 [bar]": [
        "P72"
    ],
    "P77 [bar]": [
        "P77"
    ],
    "P775 [bar]": [
        "P775"
    ],
    "P776 [bar]": [
        "P776"
    ],
    "P777 [bar]": [
        "P777"
    ],
    "P79 [bar]": [
        "P79"
    ],
    "P81 [bar]": [
        "P81"
    ],
    "P82 [bar]": [
        "P82"
    ],
    "P83 [bar]": [
        "P83"
    ],
    "P84 [bar]": [
        "P84"
    ],
    "P88 [bar]": [
        "P88"
    ],
    "PermissionToRun [-]": [
        "PermissionToRun"
    ],
    "SeaWaterTemperature [deg C]": [
        "SeaWaterTemperature"
    ],
    "SecondaryStatusWord [-]": [
        "SecondaryStatusWord"
    ],
    "StatusWord [-]": [
        "StatusWord"
    ],
    "T31 [deg C]": [
        "T31"
    ],
    "T33 [deg C]": [
        "T33"
    ],
    "T35 [deg C]": [
        "T35"
    ],
    "T36 [deg C]": [
        "T36"
    ],
    "T37 [deg C]": [
        "T37"
    ],
    "T38 [deg C]": [
        "T38"
    ],
    "T39 [deg C]": [
        "T39"
    ],
    "T41 [deg C]": [
        "T41"
    ],
    "T43 [deg C]": [
        "T43"
    ],
    "T44 [deg C]": [
        "T44"
    ],
    "T45 [deg C]": [
        "T45"
    ],
    "T46 [deg C]": [
        "T46"
    ],
    "T47 [deg C]": [
        "T47"
    ],
    "TurbSpeed [rpm]": [
        "TurbSpeed"
    ],

    # P1 old tag names
    "HT6301Running [-]": [
        "HT6301Open [-]"
    ],
    "HT6302Running [-]": [
        "HT6302Open [-]"
    ],
    "HT6306Running [-]": [
        "HT6306Open [-]"
    ],
    "N-TT853 [deg C]": [
        "TT853 [deg C]"
    ],
    "AlarmCode [-]": [
        "AlertCode [-]"
    ],
    "VX6280 [mm/s]": [
        "VX280 [mm/s]"
    ],
    "VY6281 [mm/s]": [
        "VY281 [mm/s]"
    ],
    "TT6299 [deg C]": [
        "N-TT6299 [deg C]"
    ],
    # "TT6305 [deg C]": [
    #     "OilDrainTemp [deg C]" # Historic data with both names, don't want to delete
    # ],
    "TempCFast [deg C]": [
        "Temp CFast [deg C]"
    ],
    "TempMTCX [deg C]": [
        "Temp MTCX [deg C]"
    ],
    "TempRAM [deg C]": [
        "Temp RAM [deg C]"
    ],
    "StorageWear [%]": [
        "Storage wear [%]"
    ],
}

# Correct name for each synonym
CORRECTIONS = {i: s for s, l in SYNONYMS.items() for i in l}

# Substring corrections
SUBSTRINGS = {
    "[A]": [
        "[Amp]",
        "[amp]",
    ],
    "[bar]": [
        "[Bar]",
    ],
    "[bara]": [
        "[bar a]",
        "[bar(a)]",
        "[barA]",
    ],
    "[barg]": [
        "[bar g]",
        "[bar(g)]",
    ],
    "[deg C]": [
        "[Deg C]",
        "[degC]",
        "[DegC]",
        "[deg C ]",
    ],
    "[deg]": [
        "[Deg]",
    ],
    "[kVAR]": [
        "[kvar]",
    ],
    "[kW]": [
        "[kw]",
    ],
    "[kg/s]": [
        "[Kg/s]",
    ],
    "[l/min]": [
        "[l/m]",
    ],
    "[mbar]": [
        "[mBar]",
    ],
    "[MPa]": [
        "[MPar]",
        "[Mpa]",
    ],
    "[Nm]": [
        "[N.m]",
    ],
    "[ubar]": [
        "[microb]",
    ],
    "[um]": [
        "[microm]",
    ],
    "[VAR]": [
        "[var]",
    ],
    "": [
        "Deif_"
    ],

    # P1 old tag names
    "PDT7300": [
        "N-FT298"
    ],
    "PT7180": [
        "N-PT180"
    ],
    "N-PT8181": [
        "N-PT181"
    ],
    "N-PT8182": [
        "N-PT182"
    ],
    "TT8184": [
        "N-TT184"
    ],
    "TT8185": [
        "N-TT185"
    ],
    "PT8183": [
        "N-PT183"
    ],
    "FCV7155": [
        "FCV155"
    ],
    "FCV7156": [
        "FCV156"
    ],
    "FCV6195": [
        "FCV195"
    ],
    "HT6301": [
        "HTR692"
    ],
    "N-PT8179": [
        "N-PT179"
    ],

    # Old PID
    "Measurement [-]": [
        "FilteredMeasurement [-]"
    ],
    "Setpoint [-]": [
        "WorkingSetpoint [-]"
    ],

    # Old Oil system PID
    "OilSealPID": [
        "OilSystemPID"
    ],
    "OilBearingPID": [
        "OilAxialPID"
    ]
}

SUBSTRING_CORRECTIONS = {i: s for s, l in SUBSTRINGS.items() for i in l}
REGEX_SUBSTRING = r".*(\[.*\])"

def is_bad_name(name):
    """Check if a column name is incorrect."""
    return name in CORRECTIONS

def is_bad_substring(name):
    """Check if a column name substring is incorrect."""
    return any(s in name for s in SUBSTRING_CORRECTIONS)

def correct_name(name):
    """Return the correct synonym for a column name."""
    name_strip = name.strip()
    if is_bad_name(name_strip):
        return CORRECTIONS[name_strip]
    if is_bad_substring(name_strip):
        idx = [s in name_strip for s in SUBSTRING_CORRECTIONS].index(True)
        old_sub = list(SUBSTRING_CORRECTIONS)[idx]
        new_sub = SUBSTRING_CORRECTIONS[old_sub]
        new_name = name_strip.replace(old_sub, new_sub)
        # Name might still contain bad substrings
        return correct_name(new_name)
    return name_strip

def correct_names(names):
    """Return a list of corrected names."""
    return [correct_name(name) for name in names]
