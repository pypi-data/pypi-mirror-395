from .abc_continuum_object import ABCContinuumObjectNoId


class MeasuredValue(ABCContinuumObjectNoId):
    value: float
    unit: str
