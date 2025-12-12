import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
from . import IgaMappingIntersectionUtilities as IgaMappingIntersectionUtilities, MapperUtilities as MapperUtilities, MappingIntersectionUtilities as MappingIntersectionUtilities

class BeamMapper(Kratos.Mapper):
    def __init__(self, *args, **kwargs) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
    def InverseMap(self, origin_force_variable: Kratos.Array1DVariable3, origin_moment_variable: Kratos.Array1DVariable3, destination_force_variable: Kratos.Array1DVariable3, mapping_options: Kratos.Flags = ...) -> None:
        """InverseMap(self: KratosMappingApplication.BeamMapper, origin_force_variable: Kratos.Array1DVariable3, origin_moment_variable: Kratos.Array1DVariable3, destination_force_variable: Kratos.Array1DVariable3, mapping_options: Kratos.Flags = <Kratos.Flags object at 0x7fb61499c970>) -> None"""
    def Map(self, origin_displacement_variable: Kratos.Array1DVariable3, origin_rotation_variable: Kratos.Array1DVariable3, destination_displacement_variable: Kratos.Array1DVariable3, mapping_options: Kratos.Flags = ...) -> None:
        """Map(self: KratosMappingApplication.BeamMapper, origin_displacement_variable: Kratos.Array1DVariable3, origin_rotation_variable: Kratos.Array1DVariable3, destination_displacement_variable: Kratos.Array1DVariable3, mapping_options: Kratos.Flags = <Kratos.Flags object at 0x7fb613f5ec70>) -> None"""

class KratosMappingApplication(Kratos.KratosApplication):
    def __init__(self) -> None:
        """__init__(self: KratosMappingApplication.KratosMappingApplication) -> None"""
