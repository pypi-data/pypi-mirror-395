"""
Brazing Validation Module

This module provides functions for validating brazing processes including:
- Liquidus temperature crossing detection
- Brazing stage validation
- Quality score calculation
- Thermal budget verification
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union


def detect_liquidus_crossing(
    time: np.ndarray,
    temperature: np.ndarray,
    liquidus_temp: float,
    tolerance: float = 1.0
) -> List[Dict[str, Union[int, float, str]]]:
    """
    Detect when and where the temperature crosses the material material's liquidus temperature.
    
    This is critical for brazing as it indicates when the material material melts and flows.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values (°C)
        liquidus_temp: Liquidus temperature of material material (°C)
        tolerance: Temperature tolerance for crossing detection (°C, default: 1.0)
    
    Returns:
        List of dictionaries containing crossing information:
        - 'crossing_type': 'heating' or 'cooling'
        - 'time': Time of crossing
        - 'temperature': Temperature at crossing
        - 'index': Array index of crossing
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = 20 + 5*time
        >>> crossings = detect_liquidus_crossing(time, temp, liquidus_temp=450)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    crossings = []
    lower_bound = liquidus_temp - tolerance
    upper_bound = liquidus_temp + tolerance
    
    # Track if we're above or below liquidus
    above_liquidus = temperature[0] > upper_bound
    
    for i in range(1, len(temperature)):
        current_above = temperature[i] > upper_bound
        current_below = temperature[i] < lower_bound
        
        # Check for crossing from below to above (heating)
        if not above_liquidus and current_above:
            # Interpolate exact crossing time
            if temperature[i] != temperature[i-1]:
                frac = (liquidus_temp - temperature[i-1]) / (temperature[i] - temperature[i-1])
                crossing_time = time[i-1] + frac * (time[i] - time[i-1])
            else:
                crossing_time = time[i]
            
            crossings.append({
                'crossing_type': 'heating',
                'time': crossing_time,
                'temperature': liquidus_temp,
                'index': i
            })
            above_liquidus = True
        
        # Check for crossing from above to below (cooling)
        elif above_liquidus and current_below:
            # Interpolate exact crossing time
            if temperature[i] != temperature[i-1]:
                frac = (liquidus_temp - temperature[i-1]) / (temperature[i] - temperature[i-1])
                crossing_time = time[i-1] + frac * (time[i] - time[i-1])
            else:
                crossing_time = time[i]
            
            crossings.append({
                'crossing_type': 'cooling',
                'time': crossing_time,
                'temperature': liquidus_temp,
                'index': i
            })
            above_liquidus = False
    
    return crossings


def validate_brazing_stage(
    time: np.ndarray,
    temperature: np.ndarray,
    target_temp: float,
    hold_time: float,
    temp_tolerance: float = 5.0,
    time_tolerance: float = 0.1
) -> Dict[str, Union[bool, float, str]]:
    """
    Validate if a brazing stage meets the required temperature and hold time criteria.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values (°C)
        target_temp: Target brazing temperature (°C)
        hold_time: Required hold time at target temperature (minutes)
        temp_tolerance: Acceptable temperature deviation (°C, default: 5.0)
        time_tolerance: Fractional tolerance for hold time (default: 0.1 = 10%)
    
    Returns:
        Dictionary containing validation results:
        - 'valid': Boolean indicating if stage is valid
        - 'actual_hold_time': Actual time spent in temperature range
        - 'temp_deviation': Maximum deviation from target temperature
        - 'min_temp': Minimum temperature during hold
        - 'max_temp': Maximum temperature during hold
        - 'status': Human-readable status message
    
    Example:
        >>> time = np.linspace(0, 60, 600)
        >>> temp = 600 * np.ones_like(time)
        >>> result = validate_brazing_stage(time, temp, target_temp=600, hold_time=30)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    # Find indices where temperature is within tolerance
    lower_bound = target_temp - temp_tolerance
    upper_bound = target_temp + temp_tolerance
    in_range = (temperature >= lower_bound) & (temperature <= upper_bound)
    
    if not np.any(in_range):
        return {
            'valid': False,
            'actual_hold_time': 0.0,
            'temp_deviation': np.min(np.abs(temperature - target_temp)),
            'min_temp': np.min(temperature),
            'max_temp': np.max(temperature),
            'status': 'Temperature never reached target range'
        }
    
    # Calculate actual hold time (sum of all time intervals in range)
    in_range_indices = np.where(in_range)[0]
    
    # Find continuous segments
    segments = []
    segment_start = in_range_indices[0]
    
    for i in range(1, len(in_range_indices)):
        if in_range_indices[i] != in_range_indices[i-1] + 1:
            # Gap detected, end current segment
            segment_end = in_range_indices[i-1]
            segments.append((segment_start, segment_end))
            segment_start = in_range_indices[i]
    
    # Add final segment
    segments.append((segment_start, in_range_indices[-1]))
    
    # Calculate total hold time
    actual_hold_time = sum(time[end] - time[start] for start, end in segments)
    
    # Calculate temperature statistics
    temps_in_range = temperature[in_range]
    temp_deviation = max(
        abs(target_temp - np.min(temps_in_range)),
        abs(np.max(temps_in_range) - target_temp)
    )
    
    # Validate hold time
    min_required_time = hold_time * (1 - time_tolerance)
    valid = actual_hold_time >= min_required_time
    
    if valid:
        status = f'Valid: Held for {actual_hold_time:.1f} min (required: {hold_time:.1f} min)'
    else:
        status = f'Invalid: Held for {actual_hold_time:.1f} min (required: {hold_time:.1f} min)'
    
    return {
        'valid': valid,
        'actual_hold_time': actual_hold_time,
        'temp_deviation': temp_deviation,
        'min_temp': np.min(temps_in_range),
        'max_temp': np.max(temps_in_range),
        'status': status
    }


def calculate_brazing_quality_score(
    time: np.ndarray,
    temperature: np.ndarray,
    liquidus_temp: float,
    target_temp: float,
    target_hold_time: float,
    max_temp_limit: Optional[float] = None
) -> Dict[str, Union[float, str, List]]:
    """
    Calculate an overall quality score for a brazing cycle (0-100).
    
    Considers multiple factors:
    - Liquidus crossing (did material melt?)
    - Hold time adequacy
    - Temperature stability
    - Overshoot control
    - Heating/cooling rate appropriateness
    
    Args:
        time: Array of time values
        temperature: Array of temperature values (°C)
        liquidus_temp: Liquidus temperature of material (°C)
        target_temp: Target brazing temperature (°C)
        target_hold_time: Required hold time (minutes)
        max_temp_limit: Maximum allowable temperature (°C, optional)
    
    Returns:
        Dictionary containing:
        - 'overall_score': Overall quality score (0-100)
        - 'liquidus_score': Score for liquidus crossing (0-25)
        - 'hold_time_score': Score for adequate hold time (0-30)
        - 'stability_score': Score for temperature stability (0-25)
        - 'overshoot_score': Score for overshoot control (0-20)
        - 'grade': Letter grade (A, B, C, D, F)
        - 'issues': List of identified issues
    
    Example:
        >>> score = calculate_brazing_quality_score(time, temp, 
        ...     liquidus_temp=450, target_temp=600, target_hold_time=30)
    """
    issues = []
    
    # 1. Liquidus crossing score (25 points)
    crossings = detect_liquidus_crossing(time, temperature, liquidus_temp)
    heating_crossings = [c for c in crossings if c['crossing_type'] == 'heating']
    
    if len(heating_crossings) == 0:
        liquidus_score = 0
        issues.append("material material never reached liquidus temperature")
    elif len(heating_crossings) == 1:
        liquidus_score = 25
    else:
        liquidus_score = 15
        issues.append("Multiple liquidus crossings detected (thermal cycling)")
    
    # 2. Hold time score (30 points)
    validation = validate_brazing_stage(time, temperature, target_temp, target_hold_time)
    
    if validation['actual_hold_time'] >= target_hold_time:
        hold_time_score = 30
    elif validation['actual_hold_time'] >= target_hold_time * 0.9:
        hold_time_score = 25
        issues.append(f"Hold time slightly short: {validation['actual_hold_time']:.1f} min")
    elif validation['actual_hold_time'] >= target_hold_time * 0.7:
        hold_time_score = 15
        issues.append(f"Hold time insufficient: {validation['actual_hold_time']:.1f} min")
    else:
        hold_time_score = 0
        issues.append(f"Hold time critically short: {validation['actual_hold_time']:.1f} min")
    
    # 3. Temperature stability score (25 points)
    # Check temperature variation during hold period
    in_range = (temperature >= target_temp - 10) & (temperature <= target_temp + 10)
    if np.any(in_range):
        temps_in_range = temperature[in_range]
        temp_std = np.std(temps_in_range)
        
        if temp_std < 2.0:
            stability_score = 25
        elif temp_std < 5.0:
            stability_score = 20
        elif temp_std < 10.0:
            stability_score = 10
            issues.append(f"Temperature instability: σ = {temp_std:.1f}°C")
        else:
            stability_score = 0
            issues.append(f"High temperature instability: σ = {temp_std:.1f}°C")
    else:
        stability_score = 0
        issues.append("Never reached target temperature range")
    
    # 4. Overshoot control score (20 points)
    max_temp = np.max(temperature)
    overshoot = max_temp - target_temp
    
    if max_temp_limit and max_temp > max_temp_limit:
        overshoot_score = 0
        issues.append(f"Exceeded maximum temperature limit: {max_temp:.1f}°C")
    elif overshoot < 5.0:
        overshoot_score = 20
    elif overshoot < 15.0:
        overshoot_score = 15
    elif overshoot < 30.0:
        overshoot_score = 10
        issues.append(f"Moderate overshoot: {overshoot:.1f}°C")
    else:
        overshoot_score = 0
        issues.append(f"Excessive overshoot: {overshoot:.1f}°C")
    
    # Calculate overall score
    overall_score = liquidus_score + hold_time_score + stability_score + overshoot_score
    
    # Assign letter grade
    if overall_score >= 90:
        grade = 'A'
    elif overall_score >= 80:
        grade = 'B'
    elif overall_score >= 70:
        grade = 'C'
    elif overall_score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    return {
        'overall_score': overall_score,
        'liquidus_score': liquidus_score,
        'hold_time_score': hold_time_score,
        'stability_score': stability_score,
        'overshoot_score': overshoot_score,
        'grade': grade,
        'issues': issues
    }


def check_thermal_budget(
    time: np.ndarray,
    temperature: np.ndarray,
    min_temp: float,
    max_temp: float
) -> Dict[str, Union[bool, List, float]]:
    """
    Verify that the thermal cycle stays within specified temperature envelope.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values (°C)
        min_temp: Minimum allowable temperature (°C)
        max_temp: Maximum allowable temperature (°C)
    
    Returns:
        Dictionary containing:
        - 'within_budget': Boolean indicating if all temps are within limits
        - 'violations': List of time indices where limits were exceeded
        - 'min_violation': Maximum amount below min_temp (0 if none)
        - 'max_violation': Maximum amount above max_temp (0 if none)
        - 'violation_duration': Total time spent outside limits
    
    Example:
        >>> budget = check_thermal_budget(time, temp, min_temp=400, max_temp=650)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    # Find violations
    below_min = temperature < min_temp
    above_max = temperature > max_temp
    violations = below_min | above_max
    
    violation_indices = np.where(violations)[0].tolist()
    
    # Calculate violation magnitudes
    if np.any(below_min):
        min_violation = min_temp - np.min(temperature[below_min])
    else:
        min_violation = 0.0
    
    if np.any(above_max):
        max_violation = np.max(temperature[above_max]) - max_temp
    else:
        max_violation = 0.0
    
    # Calculate violation duration
    if len(violation_indices) > 0:
        violation_duration = sum(
            time[i] - time[i-1] 
            for i in violation_indices 
            if i > 0 and violations[i-1]
        )
    else:
        violation_duration = 0.0
    
    return {
        'within_budget': len(violation_indices) == 0,
        'violations': violation_indices,
        'min_violation': min_violation,
        'max_violation': max_violation,
        'violation_duration': violation_duration
    }
