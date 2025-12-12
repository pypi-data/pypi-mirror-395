"""
Conscious Bridge Law Package
Version: 1.0.3
"""

__version__ = "1.0.3"

# إعادة تصدير المكونات الرئيسية
from ..engine.conscious_law import ConsciousBridgeLaw
from ..core.phi_calculator import PhiCalculator

__all__ = ["ConsciousBridgeLaw", "PhiCalculator", "__version__"]
