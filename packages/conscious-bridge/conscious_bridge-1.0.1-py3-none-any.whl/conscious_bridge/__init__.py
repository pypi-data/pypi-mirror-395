"""
Conscious Bridge Law - Main Package
"""

__version__ = "1.0.1"
__author__ = "Samir Baladi"

# إعادة تصدير المكونات الرئيسية
try:
    from ..engine.conscious_law import ConsciousBridgeLaw
    from ..core.phi_calculator import PhiCalculator
    
    __all__ = ["ConsciousBridgeLaw", "PhiCalculator"]
except ImportError:
    # للاستيراد بعد التثبيت
    __all__ = []
