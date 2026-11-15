"""NRE–AMM–OMEGA_CONTEXT_ENGINE.

An independent layer of control, interpretation, execution and verification for IA models: converts intent into formal instructions, validates results and decides whether an execution can continue.

Author of the architecture: Adrian Mendez Millan. Rule-based reference implementation (not a production system).
"""

from .engine import OmegaContextEngine, NRE, CycleStateMachine, States
from .nexus import AuthorizationPolicy, Nexus
from .gateway import MockProvider, ModelGateway, Executor, ExecutionTimeout
from .verification import (
    StructuralValidation,
    ReferenceVerifier,
    EvidenceVerifier,
    VerificationPipeline,
)
from .storage import Storage

__version__ = "2.0.0"
__author__ = "Adrian Mendez Millan"

__all__ = [
    "OmegaContextEngine", "NRE", "CycleStateMachine", "States",
    "AuthorizationPolicy", "Nexus", "MockProvider", "ModelGateway",
    "Executor", "ExecutionTimeout", "StructuralValidation",
    "ReferenceVerifier", "EvidenceVerifier", "VerificationPipeline",
    "Storage", "__version__",
]
