import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import os
from typing import overload

class KratosMedApplication(Kratos.KratosApplication):
    def __init__(self) -> None:
        """__init__(self: KratosMedApplication.KratosMedApplication) -> None"""

class MedModelPartIO(Kratos.IO):
    @overload
    def __init__(self, arg0: os.PathLike) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosMedApplication.MedModelPartIO, arg0: os.PathLike) -> None

        2. __init__(self: KratosMedApplication.MedModelPartIO, arg0: os.PathLike, arg1: Kratos.Flags) -> None
        """
    @overload
    def __init__(self, arg0: os.PathLike, arg1: Kratos.Flags) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosMedApplication.MedModelPartIO, arg0: os.PathLike) -> None

        2. __init__(self: KratosMedApplication.MedModelPartIO, arg0: os.PathLike, arg1: Kratos.Flags) -> None
        """

class MedTestingUtilities:
    def __init__(self, *args, **kwargs) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
    @staticmethod
    def AddGeometriesFromElements(arg0: Kratos.ModelPart) -> None:
        """AddGeometriesFromElements(arg0: Kratos.ModelPart) -> None"""
    @staticmethod
    def CheckModelPartsAreEqual(model_part_1: Kratos.ModelPart, model_part_2: Kratos.ModelPart, check_sub_model_parts: bool = ...) -> None:
        """CheckModelPartsAreEqual(model_part_1: Kratos.ModelPart, model_part_2: Kratos.ModelPart, check_sub_model_parts: bool = True) -> None"""
    @staticmethod
    def ComputeArea(arg0: Kratos.ModelPart) -> float:
        """ComputeArea(arg0: Kratos.ModelPart) -> float"""
    @staticmethod
    def ComputeDomainSize(arg0: Kratos.ModelPart) -> float:
        """ComputeDomainSize(arg0: Kratos.ModelPart) -> float"""
    @staticmethod
    def ComputeLength(arg0: Kratos.ModelPart) -> float:
        """ComputeLength(arg0: Kratos.ModelPart) -> float"""
    @staticmethod
    def ComputeVolume(arg0: Kratos.ModelPart) -> float:
        """ComputeVolume(arg0: Kratos.ModelPart) -> float"""
