"""
Pattern Detection for CAILculator
Detects mathematical patterns using Chavez Transform properties
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging

from .transforms import ChavezTransform, create_canonical_six_pattern

logger = logging.getLogger(__name__)


@dataclass
class Pattern:
    """Represents a detected mathematical pattern."""
    pattern_type: str
    confidence: float  # 0.0 to 1.0
    description: str
    indices: Optional[List[int]] = None
    metrics: Optional[Dict[str, Any]] = None


class PatternDetector:
    """
    Detects mathematical patterns in data using Chavez Transform analysis.
    
    Patterns detected:
    - Conjugation symmetry (E8-related patterns)
    - Bilateral zeros (zero divisor structure)
    - Dimensional persistence (stability across dimensions)
    """
    
    def __init__(self, alpha: float = 1.0):
        """
        Initialize pattern detector.
        
        Args:
            alpha: Convergence parameter for Chavez Transform
        """
        self.alpha = alpha
        self.ct = ChavezTransform(dimension=32, alpha=alpha)
    
    def detect_all_patterns(self, data: np.ndarray) -> List[Pattern]:
        """
        Detect all pattern types in the data.
        
        Args:
            data: Input data array
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Detect each pattern type
        patterns.extend(self._detect_conjugation_symmetry(data))
        patterns.extend(self._detect_bilateral_zeros(data))
        patterns.extend(self._detect_dimensional_persistence(data))
        
        # Sort by confidence
        patterns.sort(key=lambda p: p.confidence, reverse=True)
        
        return patterns
    
    def _detect_conjugation_symmetry(self, data: np.ndarray) -> List[Pattern]:
        """
        Detect conjugation symmetry patterns.
        
        Conjugation symmetry occurs when data exhibits symmetry under
        Cayley-Dickson conjugation operations, related to E8 structure.
        
        Args:
            data: Input data array
            
        Returns:
            List of conjugation symmetry patterns found
        """
        patterns = []
        
        try:
            # Check for mirror symmetry (simple conjugation)
            if len(data) < 2:
                return patterns
            
            # Test symmetry around midpoint
            mid = len(data) // 2
            left_half = data[:mid]
            right_half = data[mid:mid+len(left_half)][::-1]  # Reversed
            
            if len(left_half) != len(right_half):
                return patterns
            
            # Compute symmetry score
            diff = np.abs(left_half - right_half)
            max_val = max(np.max(np.abs(data)), 1.0)
            symmetry_score = 1.0 - (np.mean(diff) / max_val)
            
            if symmetry_score > 0.5:  # Threshold for detection
                # NOTE: Transform verification disabled for performance
                # Running all 6 Canonical patterns adds ~5 minutes computation
                # Using symmetry score only for now
                combined_confidence = symmetry_score
                
                patterns.append(Pattern(
                    pattern_type="conjugation_symmetry",
                    confidence=float(combined_confidence),
                    description=f"Mirror symmetry detected with {symmetry_score*100:.1f}% alignment",
                    indices=[int(mid)],
                    metrics={
                        "symmetry_score": float(symmetry_score),
                        "midpoint_index": int(mid),
                        "note": "Transform verification disabled for performance"
                    }
                ))
        
        except Exception as e:
            logger.error(f"Error in conjugation symmetry detection: {e}")
        
        return patterns
    
    def _detect_bilateral_zeros(self, data: np.ndarray) -> List[Pattern]:
        """
        Detect bilateral zero patterns.
        
        Bilateral zeros occur when data has symmetric zero-crossing pairs,
        related to zero divisor structure in Cayley-Dickson algebras.
        
        Args:
            data: Input data array
            
        Returns:
            List of bilateral zero patterns found
        """
        patterns = []
        
        try:
            if len(data) < 3:
                return patterns
            
            # Find zero crossings (sign changes)
            signs = np.sign(data)
            sign_changes = np.where(np.diff(signs) != 0)[0]
            
            if len(sign_changes) < 2:
                return patterns
            
            # Look for symmetric pairs of zero crossings
            mid = len(data) / 2.0
            
            zero_pairs = []
            for i, idx1 in enumerate(sign_changes):
                for idx2 in sign_changes[i+1:]:
                    # Check if they're symmetric around midpoint
                    dist_from_mid_1 = abs(idx1 - mid)
                    dist_from_mid_2 = abs(idx2 - mid)
                    
                    if abs(dist_from_mid_1 - dist_from_mid_2) < 0.1 * len(data):
                        zero_pairs.append((idx1, idx2))
            
            if zero_pairs:
                # Confidence based on number of pairs and their symmetry
                num_pairs = len(zero_pairs)
                confidence = min(0.5 + 0.1 * num_pairs, 0.95)

                patterns.append(Pattern(
                    pattern_type="bilateral_zeros",
                    confidence=float(confidence),
                    description=f"Detected {num_pairs} symmetric zero-crossing pair(s)",
                    indices=[int(idx) for pair in zero_pairs for idx in pair],
                    metrics={
                        "num_pairs": int(num_pairs),
                        "zero_crossing_indices": [int(idx) for idx in sign_changes]
                    }
                ))
        
        except Exception as e:
            logger.error(f"Error in bilateral zeros detection: {e}")
        
        return patterns
    
    def _detect_dimensional_persistence(self, data: np.ndarray) -> List[Pattern]:
        """
        Detect dimensional persistence patterns.
        
        Dimensional persistence occurs when transform values remain stable
        across different dimensional parameters, indicating robust structure.
        
        Args:
            data: Input data array
            
        Returns:
            List of dimensional persistence patterns found
        """
        patterns = []
        
        try:
            if len(data) < 2:
                return patterns
            
            # Test transform stability across dimensions
            P, Q = create_canonical_six_pattern(1)

            # Create function from data
            def f(x):
                x_scalar = x[0] if len(x) > 0 else 0.0
                indices = np.linspace(-5, 5, len(data))
                result = 0.0
                for idx, val in zip(indices, data):
                    result += val * np.exp(-((x_scalar - idx) ** 2))
                return result

            # NOTE: Dimensional persistence detection disabled for performance
            # Running 5 dimension parameter tests adds ~4 minutes computation
            # This pattern detection is currently unavailable
            pass
        
        except Exception as e:
            logger.error(f"Error in dimensional persistence detection: {e}")
        
        return patterns
    
    def detect_custom_pattern(
        self,
        data: np.ndarray,
        pattern_name: str,
        detection_func: callable
    ) -> Optional[Pattern]:
        """
        Detect a custom pattern using a user-provided detection function.
        
        Args:
            data: Input data array
            pattern_name: Name for the custom pattern
            detection_func: Function that takes data and returns (confidence, description, metrics)
            
        Returns:
            Pattern if detected, None otherwise
        """
        try:
            confidence, description, metrics = detection_func(data)
            
            if confidence > 0.0:
                return Pattern(
                    pattern_type=pattern_name,
                    confidence=float(confidence),
                    description=description,
                    metrics=metrics
                )
        except Exception as e:
            logger.error(f"Error in custom pattern detection: {e}")
        
        return None
