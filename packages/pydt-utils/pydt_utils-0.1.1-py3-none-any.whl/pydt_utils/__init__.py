"""
pydt_utils: Digital Twin + Brazing Utilities

A comprehensive Python library for thermal cycle analysis, brazing validation,
anomaly detection, thermal simulation, and visualization utilities.

Modules:
    - cycle: Thermal cycle analysis functions
    - brazing: Brazing validation and quality metrics
    - thermal: Thermal simulation and physics calculations
    - anomaly: Anomaly detection algorithms
    - plot: Visualization utilities
"""

__version__ = "0.1.0"
__author__ = "Manthan"
__license__ = "MIT"

# Import main functions from each module for convenient access
from .cycle import (
    calculate_ramp_rate,
    smooth_temperature_data,
    detect_soak_zones,
    segment_thermal_cycle,
)

from .brazing import (
    detect_liquidus_crossing,
    validate_brazing_stage,
    calculate_brazing_quality_score,
    check_thermal_budget,
)

from .thermal import (
    calculate_heat_flux,
    solve_1d_diffusion,
    calculate_biot_number,
    estimate_cooling_time,
)

from .anomaly import (
    detect_temperature_spikes,
    detect_overshoot,
    detect_rate_anomalies,
    statistical_anomaly_detection,
)

from .plot import (
    plot_thermal_cycle,
    plot_brazing_stages,
    plot_with_anomalies,
    plot_temperature_distribution,
    create_cycle_comparison,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Cycle functions
    "calculate_ramp_rate",
    "smooth_temperature_data",
    "detect_soak_zones",
    "segment_thermal_cycle",
    # Brazing functions
    "detect_liquidus_crossing",
    "validate_brazing_stage",
    "calculate_brazing_quality_score",
    "check_thermal_budget",
    # Thermal functions
    "calculate_heat_flux",
    "solve_1d_diffusion",
    "calculate_biot_number",
    "estimate_cooling_time",
    # Anomaly functions
    "detect_temperature_spikes",
    "detect_overshoot",
    "detect_rate_anomalies",
    "statistical_anomaly_detection",
    # Plot functions
    "plot_thermal_cycle",
    "plot_brazing_stages",
    "plot_with_anomalies",
    "plot_temperature_distribution",
    "create_cycle_comparison",
]
