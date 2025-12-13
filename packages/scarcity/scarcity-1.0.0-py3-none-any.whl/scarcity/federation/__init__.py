"""
Federated learning layer for SCARCITY.

Exposes high-level orchestrators and packet schemas used by the online,
model-free federation pipeline.
"""

from .packets import PathPack, EdgeDelta, PolicyPack, CausalSemanticPack
from .aggregator import AggregationMethod, FederatedAggregator
from .trust_scorer import TrustScorer
from .privacy_guard import PrivacyGuard
from .validator import PacketValidator
from .scheduler import FederationScheduler
from .client_agent import FederationClientAgent
from .coordinator import FederationCoordinator
from .reconciler import StoreReconciler
from .codec import PayloadCodec

__all__ = [
    "PathPack",
    "EdgeDelta",
    "PolicyPack",
    "CausalSemanticPack",
    "AggregationMethod",
    "FederatedAggregator",
    "TrustScorer",
    "PrivacyGuard",
    "PacketValidator",
    "FederationScheduler",
    "FederationClientAgent",
    "FederationCoordinator",
    "StoreReconciler",
    "PayloadCodec",
]

