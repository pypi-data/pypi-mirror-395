"""
SPAGHETTI - Structural Phase Adaptation via Generative Histological Enhancement
and Texture-preserving Translation Integration

A PyTorch implementation for phase-contrast microscopy image transformation.
"""

from spaghetti.inferences import Spaghetti
from spaghetti.dataset import TrainingDataset
from spaghetti.train import train_spaghetti
from spaghetti import utils

__all__ = [
    "Spaghetti",
    "TrainingDataset",
    "train_spaghetti",
    "utils",
]
