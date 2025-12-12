"""Builder helpers exposed by the Chronopt Python API."""

from __future__ import annotations

from chronopt._chronopt import DiffsolBuilder, ScalarBuilder, VectorBuilder

DiffsolProblemBuilder = DiffsolBuilder
ScalarProblemBuilder = ScalarBuilder
VectorProblemBuilder = VectorBuilder

__all__ = [
    "DiffsolBuilder",
    "ScalarBuilder",
    "VectorBuilder",
    "DiffsolProblemBuilder",
    "ScalarProblemBuilder",
    "VectorProblemBuilder",
]
