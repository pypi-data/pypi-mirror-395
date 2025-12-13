"""
SVM-based classification utilities for spatial transcriptomics data.

This module provides functions for analyzing SVM models, extracting feature weights,
and performing consensus-based cluster annotation.
"""

from .feature_weight_heatmap import feature_weight_heatmap
from .classes_from_probability_matrix import classes_from_probability_matrix
from .annotate_clusters_by_consensus import annotate_clusters_by_consensus
from .confusion_bubble_matrix import confusion_bubble_matrix

__all__ = [
    'feature_weight_heatmap',
    'classes_from_probability_matrix',
    'annotate_clusters_by_consensus',
    'confusion_bubble_matrix'
]
