# Re-export all types from submodules

# Base types
from .Object import Object

# Const module (basic constants and enums)
from .Const import (
    DECIDE,
    DEFAULT,
    DETERMINE,
    CURRENT,
    UNLIMITED,
    INFINITY,
    NINFINITY,
    PINFINITY,
    InsertMode,
    ScatterMode,
    NormType,
)

# Comm type
from .Comm import Comm, COMM_NULL, COMM_SELF, COMM_WORLD

# Device types
from .Device import Device, DeviceContext, DeviceType, StreamType, DeviceJoinMode

# Options
from .Options import Options

# Index Set types
from .IS import IS, ISType, LGMap

# Application Ordering types
from .AO import AO, AOType

# Section types
from .Section import Section

# Star Forest types
from .SF import SF, SFType

# DMLabel types
from .DMLabel import DMLabel

from .Mat import (
    Mat,
    MatType,
    MatOption,
    MatAssemblyType,
    MatInfoType,
    MatStructure,
    MatDuplicateOption,
    MatOrderingType,
    MatSolverType,
    MatFactorShiftType,
    MatSORType,
    MatStencil,
    NullSpace,
)

# Import type aliases from typing module
from petsc4py.typing import (
    # Scalar and Array types
    Scalar,
    ArrayBool,
    ArrayInt,
    ArrayReal,
    ArrayComplex,
    ArrayScalar,
    # Specification types
    DimsSpec,
    AccessModeSpec,
    InsertModeSpec,
    ScatterModeSpec,
    LayoutSizeSpec,
    NormTypeSpec,
    # Matrix-related types
    MatAssemblySpec,
    MatSizeSpec,
    MatBlockSizeSpec,
    CSRIndicesSpec,
    CSRSpec,
    NNZSpec,
    # Callback function types
    PetscOptionsHandlerFunction,
    MatNullFunction,
    DMCoarsenHookFunction,
    DMRestrictHookFunction,
    KSPRHSFunction,
    KSPOperatorsFunction,
    KSPConvergenceTestFunction,
    KSPMonitorFunction,
    KSPPreSolveFunction,
    KSPPostSolveFunction,
    SNESMonitorFunction,
    SNESObjFunction,
    SNESFunction,
    SNESJacobianFunction,
    SNESGuessFunction,
    SNESUpdateFunction,
    SNESLSPreFunction,
    SNESNGSFunction,
    SNESConvergedFunction,
    TSRHSFunction,
    TSRHSJacobian,
    TSRHSJacobianP,
    TSIFunction,
    TSIJacobian,
    TSIJacobianP,
    TSI2Function,
    TSI2Jacobian,
    TSI2JacobianP,
    TSMonitorFunction,
    TSPreStepFunction,
    TSPostStepFunction,
    TSIndicatorFunction,
    TSPostEventFunction,
    TAOObjectiveFunction,
    TAOGradientFunction,
    TAOObjectiveGradientFunction,
    TAOHessianFunction,
    TAOUpdateFunction,
    TAOMonitorFunction,
    TAOConvergedFunction,
    TAOJacobianFunction,
    TAOResidualFunction,
    TAOJacobianResidualFunction,
    TAOVariableBoundsFunction,
    TAOConstraintsFunction,
    TAOConstraintsJacobianFunction,
    TAOLSObjectiveFunction,
    TAOLSGradientFunction,
    TAOLSObjectiveGradientFunction,
)

from .Vec import Vec, VecType, VecOption

from .DM import DM, DMType, DMBoundaryType, DMPolytopeType, DMReorderDefaultFlag

from .DMDA import DMDA, DMDAStencilType, DMDAInterpolationType, DMDAElementType, DA

from .DMComposite import DMComposite

from .DMShell import DMShell

from .DMStag import DMStag, DMStagStencilType, DMStagStencilLocation

from .DMSwarm import (
    DMSwarm,
    DMSwarmType,
    DMSwarmMigrateType,
    DMSwarmCollectType,
    DMSwarmPICLayoutType,
    CellDM,
)

from .DMUtils import DMInterpolation

from .DMPlex import DMPlex, DMPlexTransformType, DMPlexTransform

from .DS import DS, DSType

from .DT import Quad

# FE module
from .FE import FE, FEType

# Log module
from .Log import Log, LogStage, LogClass, LogEvent

# Regressor module
from .Regressor import Regressor, RegressorType, RegressorLinearType

from .KSP import KSP, KSPType, KSPNormType, KSPConvergedReason, KSPHPDDMType

from .PC import (
    PC,
    PCType,
    PCSide,
    PCASMType,
    PCGASMType,
    PCMGType,
    PCMGCycleType,
    PCGAMGType,
    PCCompositeType,
    PCFieldSplitSchurPreType,
    PCFieldSplitSchurFactType,
    PCPatchConstructType,
    PCHPDDMCoarseCorrectionType,
    PCDeflationSpaceType,
    PCFailedReason,
)

from .Scatter import Scatter, ScatterType, ScatterMode

from .Viewer import (
    Viewer,
    ViewerType,
    ViewerFormat,
    ViewerFileMode,
    ViewerDrawSize,
    ViewerHDF5,
)

from .Random import Random, RandomType

from .SNES import (
    SNES,
    SNESType,
    SNESNormSchedule,
    SNESConvergedReason,
    SNESNewtonALCorrectionType,
    SNESLineSearch,
    SNESLineSearchType,
)

# Error module
from .Error import Error

# MatPartitioning module
from .MatPartitioning import MatPartitioning, MatPartitioningType

# Partitioner module
from .Partitioner import Partitioner, PartitionerType

# Space module
from .Space import Space, SpaceType, DualSpace, DualSpaceType

# Sys module
from .Sys import Sys

# TAO module
from .TAO import (
    TAO,
    TAOType,
    TAOConvergedReason,
    TAOBNCGType,
    TAOALMMType,
    TAOLineSearch,
    TAOLineSearchType,
    TAOLineSearchConvergedReason,
)

# TS module
from .TS import (
    TS,
    TSType,
    TSRKType,
    TSARKIMEXType,
    TSDIRKType,
    TSProblemType,
    TSEquationType,
    TSExactFinalTime,
    TSConvergedReason,
)

__all__ = [
    # Base types
    "Object",
    # Const module
    "DECIDE",
    "DEFAULT",
    "DETERMINE",
    "CURRENT",
    "UNLIMITED",
    "INFINITY",
    "NINFINITY",
    "PINFINITY",
    "InsertMode",
    "ScatterMode",
    "NormType",
    # Comm module
    "Comm",
    "COMM_NULL",
    "COMM_SELF",
    "COMM_WORLD",
    # Device module
    "Device",
    "DeviceContext",
    "DeviceType",
    "StreamType",
    "DeviceJoinMode",
    # Options module
    "Options",
    # Index Set types
    "IS",
    "ISType",
    "LGMap",
    # Application Ordering module
    "AO",
    "AOType",
    # Section module
    "Section",
    # Star Forest module
    "SF",
    "SFType",
    # DMLabel module
    "DMLabel",
    # Mat module
    "Mat",
    "MatType",
    "MatOption",
    "MatAssemblyType",
    "MatInfoType",
    "MatStructure",
    "MatDuplicateOption",
    "MatOrderingType",
    "MatSolverType",
    "MatFactorShiftType",
    "MatSORType",
    "MatStencil",
    "NullSpace",
    # Vec module
    "Vec",
    "VecType",
    "VecOption",
    # DM module
    "DM",
    "DMType",
    "DMBoundaryType",
    "DMPolytopeType",
    "DMReorderDefaultFlag",
    "FE",
    # DMDA module
    "DMDA",
    "DMDAStencilType",
    "DMDAInterpolationType",
    "DMDAElementType",
    "DA",
    # DMComposite module
    "DMComposite",
    # DMShell module
    "DMShell",
    # DMStag module
    "DMStag",
    "DMStagStencilType",
    "DMStagStencilLocation",
    # DMSwarm module
    "DMSwarm",
    "DMSwarmType",
    "DMSwarmMigrateType",
    "DMSwarmCollectType",
    "DMSwarmPICLayoutType",
    "CellDM",
    # DMUtils module
    "DMInterpolation",
    # DMPlex module
    "DMPlex",
    "DMPlexTransformType",
    "DMPlexTransform",
    # DS module
    "DS",
    "DSType",
    # DT module
    "Quad",
    # FE module
    "FEType",
    # Log module
    "Log",
    "LogStage",
    "LogClass",
    "LogEvent",
    # Regressor module
    "Regressor",
    "RegressorType",
    "RegressorLinearType",
    # KSP module
    "KSP",
    "KSPType",
    "KSPNormType",
    "KSPConvergedReason",
    "KSPHPDDMType",
    # PC module
    "PC",
    "PCType",
    "PCSide",
    "PCASMType",
    "PCGASMType",
    "PCMGType",
    "PCMGCycleType",
    "PCGAMGType",
    "PCCompositeType",
    "PCFieldSplitSchurPreType",
    "PCFieldSplitSchurFactType",
    "PCPatchConstructType",
    "PCHPDDMCoarseCorrectionType",
    "PCDeflationSpaceType",
    "PCFailedReason",
    # Scatter module
    "Scatter",
    "ScatterType",
    "ScatterMode",
    # Viewer module
    "Viewer",
    "ViewerType",
    "ViewerFormat",
    "ViewerFileMode",
    "ViewerDrawSize",
    "ViewerHDF5",
    # Random module
    "Random",
    "RandomType",
    # SNES module
    "SNES",
    "SNESType",
    "SNESNormSchedule",
    "SNESConvergedReason",
    "SNESNewtonALCorrectionType",
    "SNESLineSearch",
    "SNESLineSearchType",
    # Error module
    "Error",
    # MatPartitioning module
    "MatPartitioning",
    "MatPartitioningType",
    # Partitioner module
    "Partitioner",
    "PartitionerType",
    # Space module
    "Space",
    "SpaceType",
    "DualSpace",
    "DualSpaceType",
    # Sys module
    "Sys",
    # TAO module
    "TAO",
    "TAOType",
    "TAOConvergedReason",
    "TAOBNCGType",
    "TAOALMMType",
    "TAOLineSearch",
    "TAOLineSearchType",
    "TAOLineSearchConvergedReason",
    # TS module
    "TS",
    "TSType",
    "TSRKType",
    "TSARKIMEXType",
    "TSDIRKType",
    "TSProblemType",
    "TSEquationType",
    "TSExactFinalTime",
    "TSConvergedReason",
    # Type aliases
    "Scalar",
    "ArrayBool",
    "ArrayInt",
    "ArrayReal",
    "ArrayComplex",
    "ArrayScalar",
    "DimsSpec",
    "AccessModeSpec",
    "InsertModeSpec",
    "ScatterModeSpec",
    "LayoutSizeSpec",
    "NormTypeSpec",
    "MatAssemblySpec",
    "MatSizeSpec",
    "MatBlockSizeSpec",
    "CSRIndicesSpec",
    "CSRSpec",
    "NNZSpec",
    # Callback function types
    "PetscOptionsHandlerFunction",
    "MatNullFunction",
    "DMCoarsenHookFunction",
    "DMRestrictHookFunction",
    "KSPRHSFunction",
    "KSPOperatorsFunction",
    "KSPConvergenceTestFunction",
    "KSPMonitorFunction",
    "KSPPreSolveFunction",
    "KSPPostSolveFunction",
    "SNESMonitorFunction",
    "SNESObjFunction",
    "SNESFunction",
    "SNESJacobianFunction",
    "SNESGuessFunction",
    "SNESUpdateFunction",
    "SNESLSPreFunction",
    "SNESNGSFunction",
    "SNESConvergedFunction",
    "TSRHSFunction",
    "TSRHSJacobian",
    "TSRHSJacobianP",
    "TSIFunction",
    "TSIJacobian",
    "TSIJacobianP",
    "TSI2Function",
    "TSI2Jacobian",
    "TSI2JacobianP",
    "TSMonitorFunction",
    "TSPreStepFunction",
    "TSPostStepFunction",
    "TSIndicatorFunction",
    "TSPostEventFunction",
    "TAOObjectiveFunction",
    "TAOGradientFunction",
    "TAOObjectiveGradientFunction",
    "TAOHessianFunction",
    "TAOUpdateFunction",
    "TAOMonitorFunction",
    "TAOConvergedFunction",
    "TAOJacobianFunction",
    "TAOResidualFunction",
    "TAOJacobianResidualFunction",
    "TAOVariableBoundsFunction",
    "TAOConstraintsFunction",
    "TAOConstraintsJacobianFunction",
    "TAOLSObjectiveFunction",
    "TAOLSGradientFunction",
    "TAOLSObjectiveGradientFunction",
]
