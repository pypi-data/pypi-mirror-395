import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import KratosMultiphysics.DEMApplication as KratosDEMApplication
from typing import overload

class AdamsBashforthStrategy(KratosDEMApplication.ExplicitSolverStrategy):
    def __init__(self, arg0: KratosDEMApplication.ExplicitSolverSettings, arg1: float, arg2: float, arg3: float, arg4: int, arg5: KratosDEMApplication.ParticleCreatorDestructor, arg6: KratosDEMApplication.DEM_FEM_Search, arg7: Kratos.SpatialSearch, arg8: Kratos.Parameters) -> None:
        """__init__(self: KratosSwimmingDEMApplication.AdamsBashforthStrategy, arg0: KratosDEMApplication.ExplicitSolverSettings, arg1: float, arg2: float, arg3: float, arg4: int, arg5: KratosDEMApplication.ParticleCreatorDestructor, arg6: KratosDEMApplication.DEM_FEM_Search, arg7: Kratos.SpatialSearch, arg8: Kratos.Parameters) -> None"""

class AdditionFunction(RealFunction):
    def __init__(self, arg0: float, arg1: RealFunction, arg2: RealFunction) -> None:
        """__init__(self: KratosSwimmingDEMApplication.AdditionFunction, arg0: float, arg1: KratosSwimmingDEMApplication.RealFunction, arg2: KratosSwimmingDEMApplication.RealFunction) -> None"""
    def CalculateDerivative(self, arg0: float) -> float:
        """CalculateDerivative(self: KratosSwimmingDEMApplication.AdditionFunction, arg0: float) -> float"""
    def CalculateSecondDerivative(self, arg0: float) -> float:
        """CalculateSecondDerivative(self: KratosSwimmingDEMApplication.AdditionFunction, arg0: float) -> float"""
    def Evaluate(self, arg0: float) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.AdditionFunction, arg0: float) -> float"""

class ApplyRigidRotationProcess(Kratos.Process):
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(self: KratosSwimmingDEMApplication.ApplyRigidRotationProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None"""

class ArchimedesBuoyancyLaw(BuoyancyLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ArchimedesBuoyancyLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ArchimedesBuoyancyLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ArchimedesBuoyancyLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ArchimedesBuoyancyLaw, arg0: Kratos.Parameters) -> None
        """

class AutonHuntPrudhommeInviscidForceLaw(InviscidForceLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.AutonHuntPrudhommeInviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.AutonHuntPrudhommeInviscidForceLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.AutonHuntPrudhommeInviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.AutonHuntPrudhommeInviscidForceLaw, arg0: Kratos.Parameters) -> None
        """

class BDF2TurbulentSchemeDEMCoupled(Kratos.Scheme):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BDF2TurbulentSchemeDEMCoupled) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BDF2TurbulentSchemeDEMCoupled, arg0: Kratos.Process) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Process) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BDF2TurbulentSchemeDEMCoupled) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BDF2TurbulentSchemeDEMCoupled, arg0: Kratos.Process) -> None
        """

class BassetForceTools:
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: Kratos.Parameters) -> None"""
    def AppendIntegrands(self, arg0: Kratos.ModelPart) -> None:
        """AppendIntegrands(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: Kratos.ModelPart) -> None"""
    def AppendIntegrandsImplicit(self, arg0: Kratos.ModelPart) -> None:
        """AppendIntegrandsImplicit(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: Kratos.ModelPart) -> None"""
    def AppendIntegrandsWindow(self, arg0: Kratos.ModelPart) -> None:
        """AppendIntegrandsWindow(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: Kratos.ModelPart) -> None"""
    def FillDaitcheVectors(self, arg0: int, arg1: int, arg2: int) -> None:
        """FillDaitcheVectors(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: int, arg1: int, arg2: int) -> None"""
    def FillHinsbergVectors(self, arg0: Kratos.ModelPart, arg1: int, arg2: int) -> None:
        """FillHinsbergVectors(self: KratosSwimmingDEMApplication.BassetForceTools, arg0: Kratos.ModelPart, arg1: int, arg2: int) -> None"""

class BeetstraDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BeetstraDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BeetstraDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BeetstraDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BeetstraDragLaw, arg0: Kratos.Parameters) -> None
        """

class Bentonite_Force_Based_Inlet(KratosDEMApplication.DEM_Force_Based_Inlet):
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: int) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.Bentonite_Force_Based_Inlet, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: int) -> None

        2. __init__(self: KratosSwimmingDEMApplication.Bentonite_Force_Based_Inlet, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.Bentonite_Force_Based_Inlet, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: int) -> None

        2. __init__(self: KratosSwimmingDEMApplication.Bentonite_Force_Based_Inlet, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None
        """

class BinBasedDEMFluidCoupledMapping2D:
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    def ComputePostProcessResults(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator2D, arg4: Kratos.ProcessInfo) -> None:
        """ComputePostProcessResults(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator2D, arg4: Kratos.ProcessInfo) -> None"""
    def HomogenizeFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None:
        """HomogenizeFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None"""
    def ImposeFlowOnDEMFromField(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeFlowOnDEMFromField(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def ImposeVelocityOnDEMFromFieldToAuxVelocity(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeVelocityOnDEMFromFieldToAuxVelocity(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def InterpolateFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator2D) -> None:
        """InterpolateFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator2D) -> None"""
    def InterpolateFromFluidMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator2D, arg4: float) -> None:
        """InterpolateFromFluidMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator2D, arg4: float) -> None"""

class BinBasedDEMFluidCoupledMapping3D:
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidVariableToBeTimeFiltered(self, arg0: Kratos.DoubleVariable, arg1: float) -> None:
        """AddFluidVariableToBeTimeFiltered(*args, **kwargs)
        Overloaded function.

        1. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable, arg1: float) -> None

        2. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3, arg1: float) -> None
        """
    @overload
    def AddFluidVariableToBeTimeFiltered(self, arg0: Kratos.Array1DVariable3, arg1: float) -> None:
        """AddFluidVariableToBeTimeFiltered(*args, **kwargs)
        Overloaded function.

        1. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable, arg1: float) -> None

        2. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3, arg1: float) -> None
        """
    def ComputePostProcessResults(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator3D, arg4: Kratos.ProcessInfo) -> None:
        """ComputePostProcessResults(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator3D, arg4: Kratos.ProcessInfo) -> None"""
    def HomogenizeFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None:
        """HomogenizeFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None"""
    def ImposeFlowOnDEMFromField(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeFlowOnDEMFromField(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def ImposeVelocityOnDEMFromFieldToAuxVelocity(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeVelocityOnDEMFromFieldToAuxVelocity(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def InterpolateFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D) -> None:
        """InterpolateFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D) -> None"""
    def InterpolateFromFluidMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator3D, arg4: float) -> None:
        """InterpolateFromFluidMesh(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator3D, arg4: float) -> None"""
    def InterpolateVelocityOnAuxVelocity(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D, arg3: float) -> None:
        """InterpolateVelocityOnAuxVelocity(self: KratosSwimmingDEMApplication.BinBasedDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D, arg3: float) -> None"""

class BinBasedNanoDEMFluidCoupledMapping2D:
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.Array1DVariable3) -> None
        """
    def ComputePostProcessResults(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator2D, arg4: Kratos.ProcessInfo) -> None:
        """ComputePostProcessResults(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator2D, arg4: Kratos.ProcessInfo) -> None"""
    def HomogenizeFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None:
        """HomogenizeFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None"""
    def ImposeFlowOnDEMFromField(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeFlowOnDEMFromField(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def ImposeVelocityOnDEMFromFieldToAuxVelocity(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeVelocityOnDEMFromFieldToAuxVelocity(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def InterpolateFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator2D) -> None:
        """InterpolateFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator2D) -> None"""
    def InterpolateFromFluidMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator2D, arg4: float) -> None:
        """InterpolateFromFluidMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator2D, arg4: float) -> None"""

class BinBasedNanoDEMFluidCoupledMapping3D:
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Parameters, arg1: Kratos.SpatialSearch) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.DoubleVariable) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddDEMVariablesToImpose(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddDEMVariablesToImpose(*args, **kwargs)
        Overloaded function.

        1. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddDEMVariablesToImpose(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.DoubleVariable) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidCouplingVariable(self, arg0: Kratos.Array1DVariable3) -> None:
        """AddFluidCouplingVariable(*args, **kwargs)
        Overloaded function.

        1. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable) -> None

        2. AddFluidCouplingVariable(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3) -> None
        """
    @overload
    def AddFluidVariableToBeTimeFiltered(self, arg0: Kratos.DoubleVariable, arg1: float) -> None:
        """AddFluidVariableToBeTimeFiltered(*args, **kwargs)
        Overloaded function.

        1. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable, arg1: float) -> None

        2. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3, arg1: float) -> None
        """
    @overload
    def AddFluidVariableToBeTimeFiltered(self, arg0: Kratos.Array1DVariable3, arg1: float) -> None:
        """AddFluidVariableToBeTimeFiltered(*args, **kwargs)
        Overloaded function.

        1. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.DoubleVariable, arg1: float) -> None

        2. AddFluidVariableToBeTimeFiltered(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.Array1DVariable3, arg1: float) -> None
        """
    def ComputePostProcessResults(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator3D, arg4: Kratos.ProcessInfo) -> None:
        """ComputePostProcessResults(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.BinBasedFastPointLocator3D, arg4: Kratos.ProcessInfo) -> None"""
    def HomogenizeFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None:
        """HomogenizeFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: float, arg3: float, arg4: bool, arg5: bool) -> None"""
    def ImposeFlowOnDEMFromField(self, arg0: FluidFieldUtility, arg1: Kratos.ModelPart) -> None:
        """ImposeFlowOnDEMFromField(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: KratosSwimmingDEMApplication.FluidFieldUtility, arg1: Kratos.ModelPart) -> None"""
    def InterpolateFromDEMMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D) -> None:
        """InterpolateFromDEMMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.BinBasedFastPointLocator3D) -> None"""
    def InterpolateFromFluidMesh(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator3D, arg4: float) -> None:
        """InterpolateFromFluidMesh(self: KratosSwimmingDEMApplication.BinBasedNanoDEMFluidCoupledMapping3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.Parameters, arg3: Kratos.BinBasedFastPointLocator3D, arg4: float) -> None"""

class BoundingBoxRule(SpaceTimeRule):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BoundingBoxRule) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float) -> None
        """
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BoundingBoxRule) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float) -> None
        """
    def CheckIfRuleIsMet(self, arg0: float, arg1: float, arg2: float, arg3: float) -> bool:
        """CheckIfRuleIsMet(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float, arg2: float, arg3: float) -> bool"""
    def Info(self) -> str:
        """Info(self: KratosSwimmingDEMApplication.BoundingBoxRule) -> str"""
    def SetSpaceTimeBoundingBox(self, arg0: Kratos.Array4, arg1: Kratos.Array4) -> None:
        """SetSpaceTimeBoundingBox(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: Kratos.Array4, arg1: Kratos.Array4) -> None"""
    def SetTimeBoundingInterval(self, arg0: float, arg1: float) -> None:
        """SetTimeBoundingInterval(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float) -> None"""
    def SetXBoundingInterval(self, arg0: float, arg1: float) -> None:
        """SetXBoundingInterval(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float) -> None"""
    def SetYBoundingInterval(self, arg0: float, arg1: float) -> None:
        """SetYBoundingInterval(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float) -> None"""
    def SetZBoundingInterval(self, arg0: float, arg1: float) -> None:
        """SetZBoundingInterval(self: KratosSwimmingDEMApplication.BoundingBoxRule, arg0: float, arg1: float) -> None"""

class BoussinesqBassetHistoryForceLaw(HistoryForceLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BoussinesqBassetHistoryForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BoussinesqBassetHistoryForceLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BoussinesqBassetHistoryForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BoussinesqBassetHistoryForceLaw, arg0: Kratos.Parameters) -> None
        """

class BumpTransientPorositySolutionBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BumpTransientPorositySolutionBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BumpTransientPorositySolutionBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BumpTransientPorositySolutionBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BumpTransientPorositySolutionBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class BuoyancyLaw:
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BuoyancyLaw, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BuoyancyLaw) -> None
        """
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.BuoyancyLaw, arg0: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.BuoyancyLaw) -> None
        """
    def Clone(self) -> BuoyancyLaw:
        """Clone(self: KratosSwimmingDEMApplication.BuoyancyLaw) -> KratosSwimmingDEMApplication.BuoyancyLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.BuoyancyLaw) -> str"""
    def SetBuoyancyLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetBuoyancyLawInProperties(self: KratosSwimmingDEMApplication.BuoyancyLaw, arg0: Kratos.Properties) -> None"""

class CellularFlowField(VelocityField):
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.CellularFlowField, arg0: float, arg1: float, arg2: float, arg3: float) -> None"""

class ChienDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ChienDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ChienDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ChienDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ChienDragLaw, arg0: Kratos.Parameters) -> None
        """

class CompositionFunction(RealFunction):
    def __init__(self, arg0: float, arg1: RealFunction, arg2: RealFunction) -> None:
        """__init__(self: KratosSwimmingDEMApplication.CompositionFunction, arg0: float, arg1: KratosSwimmingDEMApplication.RealFunction, arg2: KratosSwimmingDEMApplication.RealFunction) -> None"""
    def CalculateDerivative(self, arg0: float) -> float:
        """CalculateDerivative(self: KratosSwimmingDEMApplication.CompositionFunction, arg0: float) -> float"""
    def CalculateSecondDerivative(self, arg0: float) -> float:
        """CalculateSecondDerivative(self: KratosSwimmingDEMApplication.CompositionFunction, arg0: float) -> float"""
    def Evaluate(self, arg0: float) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.CompositionFunction, arg0: float) -> float"""

class ConstantVelocityField(VelocityField):
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.ConstantVelocityField, arg0: float, arg1: float, arg2: float) -> None"""

class CustomFunctionsCalculator2D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D) -> None"""
    def AssessStationarity(self, arg0: Kratos.ModelPart, arg1: float) -> bool:
        """AssessStationarity(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart, arg1: float) -> bool"""
    def CalculateDomainVolume(self, arg0: Kratos.ModelPart) -> float:
        """CalculateDomainVolume(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart) -> float"""
    def CalculateGlobalFluidVolume(self, arg0: Kratos.ModelPart) -> float:
        """CalculateGlobalFluidVolume(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart) -> float"""
    def CalculatePressureGradient(self, arg0: Kratos.ModelPart) -> None:
        """CalculatePressureGradient(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart) -> None"""
    def CalculateTotalHydrodynamicForceOnFluid(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None:
        """CalculateTotalHydrodynamicForceOnFluid(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None"""
    def CalculateTotalHydrodynamicForceOnParticles(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None:
        """CalculateTotalHydrodynamicForceOnParticles(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator2D, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None"""

class CustomFunctionsCalculator3D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D) -> None"""
    def AssessStationarity(self, arg0: Kratos.ModelPart, arg1: float) -> bool:
        """AssessStationarity(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: float) -> bool"""
    def CalculateDomainVolume(self, arg0: Kratos.ModelPart) -> float:
        """CalculateDomainVolume(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart) -> float"""
    def CalculateGlobalFluidVolume(self, arg0: Kratos.ModelPart) -> float:
        """CalculateGlobalFluidVolume(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart) -> float"""
    def CalculatePressureGradient(self, arg0: Kratos.ModelPart) -> None:
        """CalculatePressureGradient(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart) -> None"""
    def CalculateTotalHydrodynamicForceOnFluid(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None:
        """CalculateTotalHydrodynamicForceOnFluid(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None"""
    def CalculateTotalHydrodynamicForceOnParticles(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None:
        """CalculateTotalHydrodynamicForceOnParticles(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array3) -> None"""
    @overload
    def CopyValuesFromFirstToSecond(self, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.DoubleVariable) -> None:
        """CopyValuesFromFirstToSecond(*args, **kwargs)
        Overloaded function.

        1. CopyValuesFromFirstToSecond(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.DoubleVariable) -> None

        2. CopyValuesFromFirstToSecond(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None
        """
    @overload
    def CopyValuesFromFirstToSecond(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """CopyValuesFromFirstToSecond(*args, **kwargs)
        Overloaded function.

        1. CopyValuesFromFirstToSecond(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.DoubleVariable) -> None

        2. CopyValuesFromFirstToSecond(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None
        """
    @overload
    def SetValueOfAllNotes(self, arg0: Kratos.ModelPart, arg1: float, arg2: Kratos.DoubleVariable) -> None:
        """SetValueOfAllNotes(*args, **kwargs)
        Overloaded function.

        1. SetValueOfAllNotes(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: float, arg2: Kratos.DoubleVariable) -> None

        2. SetValueOfAllNotes(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array1DVariable3) -> None
        """
    @overload
    def SetValueOfAllNotes(self, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array1DVariable3) -> None:
        """SetValueOfAllNotes(*args, **kwargs)
        Overloaded function.

        1. SetValueOfAllNotes(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: float, arg2: Kratos.DoubleVariable) -> None

        2. SetValueOfAllNotes(self: KratosSwimmingDEMApplication.CustomFunctionsCalculator3D, arg0: Kratos.ModelPart, arg1: Kratos.Array3, arg2: Kratos.Array1DVariable3) -> None
        """

class DallavalleDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.DallavalleDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.DallavalleDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.DallavalleDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.DallavalleDragLaw, arg0: Kratos.Parameters) -> None
        """

class DerivativeRecoveryMeshingTools2D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.DerivativeRecoveryMeshingTools2D) -> None"""
    def FillUpEdgesModelPartFromSimplicesModelPart(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: str) -> None:
        """FillUpEdgesModelPartFromSimplicesModelPart(self: KratosSwimmingDEMApplication.DerivativeRecoveryMeshingTools2D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: str) -> None"""

class DerivativeRecoveryMeshingTools3D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.DerivativeRecoveryMeshingTools3D) -> None"""
    def FillUpEdgesModelPartFromSimplicesModelPart(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: str) -> None:
        """FillUpEdgesModelPartFromSimplicesModelPart(self: KratosSwimmingDEMApplication.DerivativeRecoveryMeshingTools3D, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: str) -> None"""

class DerivativeRecoveryTool3D:
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None"""
    def AddTimeDerivativeComponent(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: int) -> None:
        """AddTimeDerivativeComponent(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: int) -> None"""
    def CalculateGradient(self, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.Array1DVariable3) -> None:
        """CalculateGradient(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.Array1DVariable3) -> None"""
    def CalculateVectorLaplacian(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """CalculateVectorLaplacian(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None"""
    def CalculateVectorMaterialDerivative(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None:
        """CalculateVectorMaterialDerivative(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None"""
    def CalculateVectorMaterialDerivativeComponent(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None:
        """CalculateVectorMaterialDerivativeComponent(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None"""
    def CalculateVectorMaterialDerivativeFromGradient(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3, arg5: Kratos.Array1DVariable3) -> None:
        """CalculateVectorMaterialDerivativeFromGradient(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3, arg5: Kratos.Array1DVariable3) -> None"""
    def CalculateVelocityLaplacianRate(self, arg0: Kratos.ModelPart) -> None:
        """CalculateVelocityLaplacianRate(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart) -> None"""
    def CalculateVorticityContributionOfTheGradientOfAComponent(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """CalculateVorticityContributionOfTheGradientOfAComponent(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None"""
    def CalculateVorticityFromGradient(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3) -> None:
        """CalculateVorticityFromGradient(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3) -> None"""
    def RecoverLagrangianAcceleration(self, arg0: Kratos.ModelPart) -> None:
        """RecoverLagrangianAcceleration(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart) -> None"""
    def RecoverSuperconvergentGradient(self, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.Array1DVariable3) -> None:
        """RecoverSuperconvergentGradient(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable, arg2: Kratos.Array1DVariable3) -> None"""
    def RecoverSuperconvergentLaplacian(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """RecoverSuperconvergentLaplacian(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None"""
    def RecoverSuperconvergentMatDeriv(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None:
        """RecoverSuperconvergentMatDeriv(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3) -> None"""
    def RecoverSuperconvergentMatDerivAndLaplacian(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3) -> None:
        """RecoverSuperconvergentMatDerivAndLaplacian(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3, arg3: Kratos.Array1DVariable3, arg4: Kratos.Array1DVariable3) -> None"""
    def RecoverSuperconvergentVelocityLaplacianFromGradient(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """RecoverSuperconvergentVelocityLaplacianFromGradient(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None"""
    def SmoothVectorField(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None:
        """SmoothVectorField(self: KratosSwimmingDEMApplication.DerivativeRecoveryTool3D, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3, arg2: Kratos.Array1DVariable3) -> None"""

class DragLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.DragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.DragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.DragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.DragLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> DragLaw:
        """Clone(self: KratosSwimmingDEMApplication.DragLaw) -> KratosSwimmingDEMApplication.DragLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.DragLaw) -> str"""
    def SetDragLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetDragLawInProperties(self: KratosSwimmingDEMApplication.DragLaw, arg0: Kratos.Properties) -> None"""

class ElSamniLiftLaw(VorticityInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ElSamniLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ElSamniLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ElSamniLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ElSamniLiftLaw, arg0: Kratos.Parameters) -> None
        """

class EmbeddedVolumeTool:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.EmbeddedVolumeTool) -> None"""
    def CalculateNegativeDistanceVolume(self, arg0: Kratos.ModelPart) -> float:
        """CalculateNegativeDistanceVolume(self: KratosSwimmingDEMApplication.EmbeddedVolumeTool, arg0: Kratos.ModelPart) -> float"""

class EthierFlowField(VelocityField):
    def __init__(self, arg0: float, arg1: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.EthierFlowField, arg0: float, arg1: float) -> None"""

class FieldUtility:
    def __init__(self, arg0: SpaceTimeSet, arg1: VectorField3D) -> None:
        """__init__(self: KratosSwimmingDEMApplication.FieldUtility, arg0: KratosSwimmingDEMApplication.SpaceTimeSet, arg1: KratosSwimmingDEMApplication.VectorField3D) -> None"""
    @overload
    def EvaluateFieldAtPoint(self, arg0: float, arg1: Kratos.Array3, arg2: RealField) -> float:
        """EvaluateFieldAtPoint(*args, **kwargs)
        Overloaded function.

        1. EvaluateFieldAtPoint(self: KratosSwimmingDEMApplication.FieldUtility, arg0: float, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.RealField) -> float

        2. EvaluateFieldAtPoint(self: KratosSwimmingDEMApplication.FieldUtility, arg0: float, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D) -> Kratos.Array3
        """
    @overload
    def EvaluateFieldAtPoint(self, arg0: float, arg1: Kratos.Array3, arg2: VectorField3D) -> Kratos.Array3:
        """EvaluateFieldAtPoint(*args, **kwargs)
        Overloaded function.

        1. EvaluateFieldAtPoint(self: KratosSwimmingDEMApplication.FieldUtility, arg0: float, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.RealField) -> float

        2. EvaluateFieldAtPoint(self: KratosSwimmingDEMApplication.FieldUtility, arg0: float, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D) -> Kratos.Array3
        """
    @overload
    def ImposeFieldOnNodes(self, arg0: Kratos.DoubleVariable, arg1: float, arg2: RealField, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None:
        """ImposeFieldOnNodes(*args, **kwargs)
        Overloaded function.

        1. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.DoubleVariable, arg1: float, arg2: KratosSwimmingDEMApplication.RealField, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        2. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.Array1DVariable3, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        3. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos::VariablesList) -> None

        4. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> None
        """
    @overload
    def ImposeFieldOnNodes(self, arg0: Kratos.Array1DVariable3, arg1: Kratos.Array3, arg2: VectorField3D, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None:
        """ImposeFieldOnNodes(*args, **kwargs)
        Overloaded function.

        1. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.DoubleVariable, arg1: float, arg2: KratosSwimmingDEMApplication.RealField, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        2. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.Array1DVariable3, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        3. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos::VariablesList) -> None

        4. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> None
        """
    @overload
    def ImposeFieldOnNodes(self, arg0: Kratos.ModelPart, arg1) -> None:
        """ImposeFieldOnNodes(*args, **kwargs)
        Overloaded function.

        1. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.DoubleVariable, arg1: float, arg2: KratosSwimmingDEMApplication.RealField, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        2. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.Array1DVariable3, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        3. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos::VariablesList) -> None

        4. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> None
        """
    @overload
    def ImposeFieldOnNodes(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> None:
        """ImposeFieldOnNodes(*args, **kwargs)
        Overloaded function.

        1. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.DoubleVariable, arg1: float, arg2: KratosSwimmingDEMApplication.RealField, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        2. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.Array1DVariable3, arg1: Kratos.Array3, arg2: KratosSwimmingDEMApplication.VectorField3D, arg3: Kratos.ModelPart, arg4: Kratos.ProcessInfo, arg5: bool) -> None

        3. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos::VariablesList) -> None

        4. ImposeFieldOnNodes(self: KratosSwimmingDEMApplication.FieldUtility, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> None
        """

class FlowStationarityCheck:
    def __init__(self, arg0: Kratos.ModelPart, arg1: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.FlowStationarityCheck, arg0: Kratos.ModelPart, arg1: float) -> None"""
    def AssessStationarity(self) -> bool:
        """AssessStationarity(self: KratosSwimmingDEMApplication.FlowStationarityCheck) -> bool"""
    def GetCharacteristicPressureDerivative(self) -> float:
        """GetCharacteristicPressureDerivative(self: KratosSwimmingDEMApplication.FlowStationarityCheck) -> float"""
    def GetCurrentPressureDerivative(self) -> float:
        """GetCurrentPressureDerivative(self: KratosSwimmingDEMApplication.FlowStationarityCheck) -> float"""
    def GetTolerance(self) -> float:
        """GetTolerance(self: KratosSwimmingDEMApplication.FlowStationarityCheck) -> float"""
    def GetTransienceMeasure(self) -> float:
        """GetTransienceMeasure(self: KratosSwimmingDEMApplication.FlowStationarityCheck) -> float"""

class FluidFieldUtility(FieldUtility):
    def __init__(self, arg0: SpaceTimeSet, arg1: VelocityField, arg2: float, arg3: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.FluidFieldUtility, arg0: KratosSwimmingDEMApplication.SpaceTimeSet, arg1: KratosSwimmingDEMApplication.VelocityField, arg2: float, arg3: float) -> None"""

class GanserDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.GanserDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.GanserDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.GanserDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.GanserDragLaw, arg0: Kratos.Parameters) -> None
        """

class HaiderAndLevenspielDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HaiderAndLevenspielDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HaiderAndLevenspielDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HaiderAndLevenspielDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HaiderAndLevenspielDragLaw, arg0: Kratos.Parameters) -> None
        """

class HistoryForceLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HistoryForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HistoryForceLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HistoryForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HistoryForceLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> HistoryForceLaw:
        """Clone(self: KratosSwimmingDEMApplication.HistoryForceLaw) -> KratosSwimmingDEMApplication.HistoryForceLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.HistoryForceLaw) -> str"""
    def SetHistoryForceLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetHistoryForceLawInProperties(self: KratosSwimmingDEMApplication.HistoryForceLaw, arg0: Kratos.Properties) -> None"""

class HybridBashforthScheme(KratosDEMApplication.SymplecticEulerScheme):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.HybridBashforthScheme) -> None"""

class HydrodynamicInteractionLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None
        """
    def Clone(self) -> HydrodynamicInteractionLaw:
        """Clone(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw) -> KratosSwimmingDEMApplication.HydrodynamicInteractionLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw) -> str"""
    def SetBuoyancyLaw(self, arg0) -> None:
        """SetBuoyancyLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::BuoyancyLaw) -> None"""
    def SetDragLaw(self, arg0) -> None:
        """SetDragLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::DragLaw) -> None"""
    def SetHistoryForceLaw(self, arg0) -> None:
        """SetHistoryForceLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::HistoryForceLaw) -> None"""
    def SetHydrodynamicInteractionLawInProperties(self, arg0: Kratos.Properties, arg1: bool) -> None:
        """SetHydrodynamicInteractionLawInProperties(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos.Properties, arg1: bool) -> None"""
    def SetInviscidForceLaw(self, arg0) -> None:
        """SetInviscidForceLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::InviscidForceLaw) -> None"""
    def SetRotationInducedLiftLaw(self, arg0) -> None:
        """SetRotationInducedLiftLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::RotationInducedLiftLaw) -> None"""
    def SetSteadyViscousTorqueLaw(self, arg0) -> None:
        """SetSteadyViscousTorqueLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::SteadyViscousTorqueLaw) -> None"""
    def SetVorticityInducedLiftLaw(self, arg0) -> None:
        """SetVorticityInducedLiftLaw(self: KratosSwimmingDEMApplication.HydrodynamicInteractionLaw, arg0: Kratos::VorticityInducedLiftLaw) -> None"""

class HyperbolicTangentialPorositySolutionAndBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class HyperbolicTangentialPorositySolutionTransientBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.HyperbolicTangentialPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class InviscidForceLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.InviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.InviscidForceLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.InviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.InviscidForceLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> InviscidForceLaw:
        """Clone(self: KratosSwimmingDEMApplication.InviscidForceLaw) -> KratosSwimmingDEMApplication.InviscidForceLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.InviscidForceLaw) -> str"""
    def SetInviscidForceLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetInviscidForceLawInProperties(self: KratosSwimmingDEMApplication.InviscidForceLaw, arg0: Kratos.Properties) -> None"""

class KratosSwimmingDEMApplication(Kratos.KratosApplication):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.KratosSwimmingDEMApplication) -> None"""

class L2ErrorNormCalculator:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.L2ErrorNormCalculator) -> None"""
    def ComputeDofsErrors(self, arg0: Kratos.ModelPart) -> None:
        """ComputeDofsErrors(self: KratosSwimmingDEMApplication.L2ErrorNormCalculator, arg0: Kratos.ModelPart) -> None"""
    def GetL2ScalarErrorNorm(self, arg0: Kratos.ModelPart) -> float:
        """GetL2ScalarErrorNorm(self: KratosSwimmingDEMApplication.L2ErrorNormCalculator, arg0: Kratos.ModelPart) -> float"""
    def GetL2VectorErrorNorm(self, arg0: Kratos.ModelPart) -> float:
        """GetL2VectorErrorNorm(self: KratosSwimmingDEMApplication.L2ErrorNormCalculator, arg0: Kratos.ModelPart) -> float"""

class LinearFunction(RealFunction):
    def __init__(self, arg0: float, arg1: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.LinearFunction, arg0: float, arg1: float) -> None"""
    def CalculateDerivative(self, arg0: float) -> float:
        """CalculateDerivative(self: KratosSwimmingDEMApplication.LinearFunction, arg0: float) -> float"""
    def CalculateSecondDerivative(self, arg0: float) -> float:
        """CalculateSecondDerivative(self: KratosSwimmingDEMApplication.LinearFunction, arg0: float) -> float"""
    def Evaluate(self, arg0: float) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.LinearFunction, arg0: float) -> float"""

class LinearRealField(RealField):
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: RealFunction, arg4: RealFunction, arg5: RealFunction) -> None:
        """__init__(self: KratosSwimmingDEMApplication.LinearRealField, arg0: float, arg1: float, arg2: float, arg3: KratosSwimmingDEMApplication.RealFunction, arg4: KratosSwimmingDEMApplication.RealFunction, arg5: KratosSwimmingDEMApplication.RealFunction) -> None"""
    def CalculateTimeDerivative(self, arg0: float, arg1: Kratos.Array3) -> float:
        """CalculateTimeDerivative(self: KratosSwimmingDEMApplication.LinearRealField, arg0: float, arg1: Kratos.Array3) -> float"""
    def Evaluate(self, arg0: float, arg1: Kratos.Array3) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.LinearRealField, arg0: float, arg1: Kratos.Array3) -> float"""

class LothRotationInducedLiftLaw(RotationInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.LothRotationInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.LothRotationInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.LothRotationInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.LothRotationInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """

class LothSteadyViscousTorqueLaw(SteadyViscousTorqueLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.LothSteadyViscousTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.LothSteadyViscousTorqueLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.LothSteadyViscousTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.LothSteadyViscousTorqueLaw, arg0: Kratos.Parameters) -> None
        """

class MeiLiftLaw(VorticityInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.MeiLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.MeiLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.MeiLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.MeiLiftLaw, arg0: Kratos.Parameters) -> None
        """

class MeshRotationUtility:
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(self: KratosSwimmingDEMApplication.MeshRotationUtility, arg0: Kratos.Parameters) -> None"""
    def RotateDEMMesh(self, arg0: Kratos.ModelPart, arg1: float) -> None:
        """RotateDEMMesh(self: KratosSwimmingDEMApplication.MeshRotationUtility, arg0: Kratos.ModelPart, arg1: float) -> None"""
    def RotateFluidVelocities(self, arg0: float) -> None:
        """RotateFluidVelocities(self: KratosSwimmingDEMApplication.MeshRotationUtility, arg0: float) -> None"""
    def RotateMesh(self, arg0: Kratos.ModelPart, arg1: float) -> None:
        """RotateMesh(self: KratosSwimmingDEMApplication.MeshRotationUtility, arg0: Kratos.ModelPart, arg1: float) -> None"""
    def SetStationaryField(self, arg0: Kratos.ModelPart, arg1: float) -> None:
        """SetStationaryField(self: KratosSwimmingDEMApplication.MeshRotationUtility, arg0: Kratos.ModelPart, arg1: float) -> None"""

class MoreThanRule(SpaceTimeRule):
    @overload
    def __init__(self, arg0: float, arg1: RealField) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.MoreThanRule, arg0: float, arg1: KratosSwimmingDEMApplication.RealField) -> None

        2. __init__(self: KratosSwimmingDEMApplication.MoreThanRule, arg0: KratosSwimmingDEMApplication.RealField, arg1: KratosSwimmingDEMApplication.RealField) -> None
        """
    @overload
    def __init__(self, arg0: RealField, arg1: RealField) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.MoreThanRule, arg0: float, arg1: KratosSwimmingDEMApplication.RealField) -> None

        2. __init__(self: KratosSwimmingDEMApplication.MoreThanRule, arg0: KratosSwimmingDEMApplication.RealField, arg1: KratosSwimmingDEMApplication.RealField) -> None
        """
    def CheckIfRuleIsMet(self, arg0: float, arg1: float, arg2: float, arg3: float) -> bool:
        """CheckIfRuleIsMet(self: KratosSwimmingDEMApplication.MoreThanRule, arg0: float, arg1: float, arg2: float, arg3: float) -> bool"""

class NewtonDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.NewtonDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.NewtonDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.NewtonDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.NewtonDragLaw, arg0: Kratos.Parameters) -> None
        """

class OesterleAndDinhLiftLaw(RotationInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.OesterleAndDinhLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.OesterleAndDinhLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.OesterleAndDinhLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.OesterleAndDinhLiftLaw, arg0: Kratos.Parameters) -> None
        """

class PorositySolutionAndBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class PorositySolutionAndSinusoidalBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndSinusoidalBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndSinusoidalBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndSinusoidalBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionAndSinusoidalBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class PorositySolutionTransientBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class PouliotFlowField(VelocityField):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.PouliotFlowField) -> None"""

class PouliotFlowField2D(VelocityField):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.PouliotFlowField2D) -> None"""

class PowerFunction(RealFunction):
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.PowerFunction, arg0: float, arg1: float, arg2: float) -> None"""
    def CalculateDerivative(self, arg0: float) -> float:
        """CalculateDerivative(self: KratosSwimmingDEMApplication.PowerFunction, arg0: float) -> float"""
    def CalculateSecondDerivative(self, arg0: float) -> float:
        """CalculateSecondDerivative(self: KratosSwimmingDEMApplication.PowerFunction, arg0: float) -> float"""
    def Evaluate(self, arg0: float) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.PowerFunction, arg0: float) -> float"""

class PowerLawFluidHydrodynamicInteractionLaw(HydrodynamicInteractionLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PowerLawFluidHydrodynamicInteractionLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PowerLawFluidHydrodynamicInteractionLaw, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.PowerLawFluidHydrodynamicInteractionLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.PowerLawFluidHydrodynamicInteractionLaw, arg0: Kratos.Properties, arg1: Kratos.Parameters) -> None
        """

class RealField:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.RealField) -> None"""

class RealFunction:
    def __init__(self, arg0: float, arg1: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.RealFunction, arg0: float, arg1: float) -> None"""
    def CalculateDerivative(self, arg0: float) -> float:
        """CalculateDerivative(self: KratosSwimmingDEMApplication.RealFunction, arg0: float) -> float"""
    def CalculateSecondDerivative(self, arg0: float) -> float:
        """CalculateSecondDerivative(self: KratosSwimmingDEMApplication.RealFunction, arg0: float) -> float"""
    def Evaluate(self, arg0: float) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.RealFunction, arg0: float) -> float"""

class RelaxedResidualBasedNewtonRaphsonStrategy(Kratos.ResidualBasedNewtonRaphsonStrategy):
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: int, arg5: bool, arg6: bool, arg7: bool) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.Parameters) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.ConvergenceCriteria, arg3: Kratos.BuilderAndSolver, arg4: Kratos.Parameters) -> None

        6. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: int, arg6: bool, arg7: bool, arg8: bool) -> None

        7. __init__(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.ConvergenceCriteria, arg4: Kratos.BuilderAndSolver, arg5: Kratos.Parameters) -> None
        """
    def GetInitializePerformedFlag(self) -> bool:
        """GetInitializePerformedFlag(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy) -> bool"""
    def GetKeepSystemConstantDuringIterations(self) -> bool:
        """GetKeepSystemConstantDuringIterations(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy) -> bool"""
    def GetMaxIterationNumber(self) -> int:
        """GetMaxIterationNumber(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy) -> int"""
    def GetUseOldStiffnessInFirstIterationFlag(self) -> bool:
        """GetUseOldStiffnessInFirstIterationFlag(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy) -> bool"""
    def SetInitializePerformedFlag(self, arg0: bool) -> None:
        """SetInitializePerformedFlag(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: bool) -> None"""
    def SetKeepSystemConstantDuringIterations(self, arg0: bool) -> None:
        """SetKeepSystemConstantDuringIterations(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: bool) -> None"""
    def SetMaxIterationNumber(self, arg0: int) -> None:
        """SetMaxIterationNumber(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: int) -> None"""
    def SetUseOldStiffnessInFirstIterationFlag(self, arg0: bool) -> None:
        """SetUseOldStiffnessInFirstIterationFlag(self: KratosSwimmingDEMApplication.RelaxedResidualBasedNewtonRaphsonStrategy, arg0: bool) -> None"""

class RenumberingNodesUtility:
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None

        3. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart) -> None

        4. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart) -> None

        5. __init__(self: KratosSwimmingDEMApplication.RenumberingNodesUtility, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart, arg2: Kratos.ModelPart, arg3: Kratos.ModelPart, arg4: Kratos.ModelPart) -> None
        """
    def Renumber(self) -> None:
        """Renumber(self: KratosSwimmingDEMApplication.RenumberingNodesUtility) -> None"""
    def UndoRenumber(self) -> None:
        """UndoRenumber(self: KratosSwimmingDEMApplication.RenumberingNodesUtility) -> None"""

class ResidualBasedDerivativeRecoveryStrategy(Kratos.ResidualBasedLinearStrategy):
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.BuilderAndSolver, arg4: bool, arg5: bool, arg6: bool, arg7: bool) -> None:
        """__init__(self: KratosSwimmingDEMApplication.ResidualBasedDerivativeRecoveryStrategy, arg0: Kratos.ModelPart, arg1: Kratos.Scheme, arg2: Kratos.LinearSolver, arg3: Kratos.BuilderAndSolver, arg4: bool, arg5: bool, arg6: bool, arg7: bool) -> None"""
    def GetResidualNorm(self) -> float:
        """GetResidualNorm(self: KratosSwimmingDEMApplication.ResidualBasedDerivativeRecoveryStrategy) -> float"""
    def SetBuilderAndSolver(self, arg0: Kratos.BuilderAndSolver) -> None:
        """SetBuilderAndSolver(self: KratosSwimmingDEMApplication.ResidualBasedDerivativeRecoveryStrategy, arg0: Kratos.BuilderAndSolver) -> None"""

class ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled(Kratos.Scheme):
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: int, arg3: Kratos.Process) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int, arg3: Kratos.Process) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int) -> None

        3. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: int, arg2: Kratos.IntegerVariable) -> None
        """
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: int) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int, arg3: Kratos.Process) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int) -> None

        3. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: int, arg2: Kratos.IntegerVariable) -> None
        """
    @overload
    def __init__(self, arg0: float, arg1: int, arg2: Kratos.IntegerVariable) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int, arg3: Kratos.Process) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: float, arg2: int) -> None

        3. __init__(self: KratosSwimmingDEMApplication.ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulentDEMCoupled, arg0: float, arg1: int, arg2: Kratos.IntegerVariable) -> None
        """

class RotationInducedLiftLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> RotationInducedLiftLaw:
        """Clone(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw) -> KratosSwimmingDEMApplication.RotationInducedLiftLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw) -> str"""
    def SetRotationInducedLiftLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetRotationInducedLiftLawInProperties(self: KratosSwimmingDEMApplication.RotationInducedLiftLaw, arg0: Kratos.Properties) -> None"""

class RubinowAndKellerLiftLaw(RotationInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerLiftLaw, arg0: Kratos.Parameters) -> None
        """

class RubinowAndKellerTorqueLaw(SteadyViscousTorqueLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerTorqueLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.RubinowAndKellerTorqueLaw, arg0: Kratos.Parameters) -> None
        """

class SaffmanLiftLaw(VorticityInducedLiftLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SaffmanLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SaffmanLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SaffmanLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SaffmanLiftLaw, arg0: Kratos.Parameters) -> None
        """

class SchillerAndNaumannDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SchillerAndNaumannDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SchillerAndNaumannDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SchillerAndNaumannDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SchillerAndNaumannDragLaw, arg0: Kratos.Parameters) -> None
        """

class ShahDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ShahDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ShahDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ShahDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ShahDragLaw, arg0: Kratos.Parameters) -> None
        """

class ShearFlow1DWithExponentialViscosityField(VelocityField):
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.ShearFlow1DWithExponentialViscosityField, arg0: float, arg1: float, arg2: float) -> None"""
    def SetRimZoneThickness(self, arg0: float) -> None:
        """SetRimZoneThickness(self: KratosSwimmingDEMApplication.ShearFlow1DWithExponentialViscosityField, arg0: float) -> None"""

class SinusoidalPorositySolutionAndBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionAndBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class SinusoidalPorositySolutionTransientBodyForceProcess(Kratos.Process):
    @overload
    def __init__(self, arg0: Kratos.ModelPart) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SinusoidalPorositySolutionTransientBodyForceProcess, arg0: Kratos.ModelPart, arg1: Kratos.Parameters) -> None
        """

class SpaceTimeRule:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.SpaceTimeRule) -> None"""

class SpaceTimeSet:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> None"""
    def AddAndRule(self, arg0: SpaceTimeRule) -> None:
        """AddAndRule(self: KratosSwimmingDEMApplication.SpaceTimeSet, arg0: KratosSwimmingDEMApplication.SpaceTimeRule) -> None"""
    def AddAndRules(self, arg0: list[SpaceTimeRule]) -> None:
        """AddAndRules(self: KratosSwimmingDEMApplication.SpaceTimeSet, arg0: list[KratosSwimmingDEMApplication.SpaceTimeRule]) -> None"""
    def AddOrRule(self, arg0: SpaceTimeRule) -> None:
        """AddOrRule(self: KratosSwimmingDEMApplication.SpaceTimeSet, arg0: KratosSwimmingDEMApplication.SpaceTimeRule) -> None"""
    def AddOrRules(self, arg0: list[SpaceTimeRule]) -> None:
        """AddOrRules(self: KratosSwimmingDEMApplication.SpaceTimeSet, arg0: list[KratosSwimmingDEMApplication.SpaceTimeRule]) -> None"""
    def GetHighTime(self) -> float:
        """GetHighTime(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetHighX(self) -> float:
        """GetHighX(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetHighY(self) -> float:
        """GetHighY(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetHighZ(self) -> float:
        """GetHighZ(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetLowTime(self) -> float:
        """GetLowTime(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetLowX(self) -> float:
        """GetLowX(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetLowY(self) -> float:
        """GetLowY(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetLowZ(self) -> float:
        """GetLowZ(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> float"""
    def GetRules(self) -> list[list[SpaceTimeRule]]:
        """GetRules(self: KratosSwimmingDEMApplication.SpaceTimeSet) -> list[list[KratosSwimmingDEMApplication.SpaceTimeRule]]"""

class SteadyViscousTorqueLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> SteadyViscousTorqueLaw:
        """Clone(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw) -> KratosSwimmingDEMApplication.SteadyViscousTorqueLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw) -> str"""
    def SetSteadyViscousTorqueLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetSteadyViscousTorqueLawInProperties(self: KratosSwimmingDEMApplication.SteadyViscousTorqueLaw, arg0: Kratos.Properties) -> None"""

class StokesDragLaw(DragLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.StokesDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.StokesDragLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.StokesDragLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.StokesDragLaw, arg0: Kratos.Parameters) -> None
        """

class SwimmingDemInPfemUtils:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.SwimmingDemInPfemUtils) -> None"""
    def TransferWalls(self, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None:
        """TransferWalls(self: KratosSwimmingDEMApplication.SwimmingDemInPfemUtils, arg0: Kratos.ModelPart, arg1: Kratos.ModelPart) -> None"""

class SymplecticEulerOldVelocityScheme(KratosDEMApplication.SymplecticEulerScheme):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.SymplecticEulerOldVelocityScheme) -> None"""

class TerminalVelocityScheme(HybridBashforthScheme):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.TerminalVelocityScheme) -> None"""

class TimeDependantForceField(VectorField3D):
    def __init__(self, arg0: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.TimeDependantForceField, arg0: float) -> None"""
    def Evaluate(self, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3, arg3: int) -> None:
        """Evaluate(self: KratosSwimmingDEMApplication.TimeDependantForceField, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3, arg3: int) -> None"""
    def GetPorosityField(self) -> TimeDependantPorosityField:
        """GetPorosityField(self: KratosSwimmingDEMApplication.TimeDependantForceField) -> KratosSwimmingDEMApplication.TimeDependantPorosityField"""

class TimeDependantPorosityField(RealField):
    def __init__(self, arg0: float) -> None:
        """__init__(self: KratosSwimmingDEMApplication.TimeDependantPorosityField, arg0: float) -> None"""
    def CalculateGradient(self, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None:
        """CalculateGradient(self: KratosSwimmingDEMApplication.TimeDependantPorosityField, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None"""
    def CalculateLaplacian(self, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None:
        """CalculateLaplacian(self: KratosSwimmingDEMApplication.TimeDependantPorosityField, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Array3) -> None"""
    def CalculateTimeDerivative(self, arg0: float, arg1: Kratos.Array3) -> float:
        """CalculateTimeDerivative(self: KratosSwimmingDEMApplication.TimeDependantPorosityField, arg0: float, arg1: Kratos.Array3) -> float"""
    def Evaluate(self, arg0: float, arg1: Kratos.Array3) -> float:
        """Evaluate(self: KratosSwimmingDEMApplication.TimeDependantPorosityField, arg0: float, arg1: Kratos.Array3) -> float"""

class VariableChecker:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.VariableChecker) -> None"""
    @overload
    def ModelPartHasNodalVariableOrNot(self, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable) -> bool:
        """ModelPartHasNodalVariableOrNot(*args, **kwargs)
        Overloaded function.

        1. ModelPartHasNodalVariableOrNot(self: KratosSwimmingDEMApplication.VariableChecker, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable) -> bool

        2. ModelPartHasNodalVariableOrNot(self: KratosSwimmingDEMApplication.VariableChecker, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> bool
        """
    @overload
    def ModelPartHasNodalVariableOrNot(self, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> bool:
        """ModelPartHasNodalVariableOrNot(*args, **kwargs)
        Overloaded function.

        1. ModelPartHasNodalVariableOrNot(self: KratosSwimmingDEMApplication.VariableChecker, arg0: Kratos.ModelPart, arg1: Kratos.DoubleVariable) -> bool

        2. ModelPartHasNodalVariableOrNot(self: KratosSwimmingDEMApplication.VariableChecker, arg0: Kratos.ModelPart, arg1: Kratos.Array1DVariable3) -> bool
        """

class VectorField2D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.VectorField2D) -> None"""

class VectorField3D:
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.VectorField3D) -> None"""

class VelocityField(VectorField3D):
    def __init__(self) -> None:
        """__init__(self: KratosSwimmingDEMApplication.VelocityField) -> None"""
    def CalculateDivergence(self, arg0: float, arg1: Kratos.Vector, arg2: int) -> float:
        """CalculateDivergence(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Vector, arg2: int) -> float"""
    def CalculateGradient(self, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Vector, arg3: Kratos.Vector, arg4: Kratos.Vector, arg5: int) -> None:
        """CalculateGradient(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Array3, arg2: Kratos.Vector, arg3: Kratos.Vector, arg4: Kratos.Vector, arg5: int) -> None"""
    def CalculateLaplacian(self, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None:
        """CalculateLaplacian(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None"""
    def CalculateMaterialAcceleration(self, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None:
        """CalculateMaterialAcceleration(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None"""
    def CalculateRotational(self, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None:
        """CalculateRotational(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None"""
    def CalculateTimeDerivative(self, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None:
        """CalculateTimeDerivative(self: KratosSwimmingDEMApplication.VelocityField, arg0: float, arg1: Kratos.Vector, arg2: Kratos.Vector, arg3: int) -> None"""

class VorticityInducedLiftLaw:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw, arg0: Kratos.Parameters) -> None
        """
    def Clone(self) -> VorticityInducedLiftLaw:
        """Clone(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw) -> KratosSwimmingDEMApplication.VorticityInducedLiftLaw"""
    def GetTypeOfLaw(self) -> str:
        """GetTypeOfLaw(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw) -> str"""
    def SetVorticityInducedLiftLawInProperties(self, arg0: Kratos.Properties) -> None:
        """SetVorticityInducedLiftLawInProperties(self: KratosSwimmingDEMApplication.VorticityInducedLiftLaw, arg0: Kratos.Properties) -> None"""

class ZuberInviscidForceLaw(InviscidForceLaw):
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ZuberInviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ZuberInviscidForceLaw, arg0: Kratos.Parameters) -> None
        """
    @overload
    def __init__(self, arg0: Kratos.Parameters) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: KratosSwimmingDEMApplication.ZuberInviscidForceLaw) -> None

        2. __init__(self: KratosSwimmingDEMApplication.ZuberInviscidForceLaw, arg0: Kratos.Parameters) -> None
        """
