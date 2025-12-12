"""
Thermal Cycle Analysis Module

This module provides functions for analyzing thermal cycles including:
- Ramp rate calculations
- Temperature data smoothing
- Soak zone detection
- Cycle segmentation into stages
"""

import numpy as np
from scipy.signal import savgol_filter
from typing import List, Tuple, Dict, Optional, Union


def calculate_ramp_rate(
    time: np.ndarray,
    temperature: np.ndarray,
    window_size: int = 5
) -> np.ndarray:
    """
    Calculate the heating/cooling rate (ramp rate) from temperature-time data.
    
    Uses central difference method with optional smoothing window to reduce noise.
    
    Args:
        time: Array of time values (seconds or minutes)
        temperature: Array of temperature values (°C or K)
        window_size: Number of points for moving average smoothing (default: 5)
    
    Returns:
        Array of ramp rates (°C/min or K/min) same length as input
    
    Example:
        >>> time = np.linspace(0, 100, 100)
        >>> temp = 20 + 5 * time  # Linear heating at 5°C/min
        >>> rates = calculate_ramp_rate(time, temp)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    if len(time) < 2:
        raise ValueError("Need at least 2 data points to calculate ramp rate")
    
    # Calculate derivative using central differences
    dt = np.diff(time)
    dT = np.diff(temperature)
    
    # Handle division by zero
    dt[dt == 0] = 1e-10
    
    # Calculate instantaneous rates
    rates = dT / dt
    
    # Pad to match original length (forward difference for last point)
    rates = np.append(rates, rates[-1])
    
    # Apply moving average smoothing if window_size > 1
    if window_size > 1:
        window_size = min(window_size, len(rates))
        if window_size % 2 == 0:
            window_size += 1  # Ensure odd window size
        rates = np.convolve(rates, np.ones(window_size)/window_size, mode='same')
    
    return rates


def smooth_temperature_data(
    temperature: np.ndarray,
    window_size: int = 11,
    method: str = 'savgol',
    polyorder: int = 3
) -> np.ndarray:
    """
    Smooth temperature data using various filtering methods.
    
    Args:
        temperature: Array of temperature values
        window_size: Size of the smoothing window (must be odd for savgol)
        method: Smoothing method - 'savgol' (Savitzky-Golay) or 'moving_avg'
        polyorder: Polynomial order for Savitzky-Golay filter (default: 3)
    
    Returns:
        Smoothed temperature array
    
    Example:
        >>> noisy_temp = np.array([100, 102, 101, 103, 150, 104, 105])
        >>> smooth_temp = smooth_temperature_data(noisy_temp, window_size=5, method='moving_avg')
    """
    if len(temperature) < window_size:
        raise ValueError(f"Data length ({len(temperature)}) must be >= window_size ({window_size})")
    
    if method == 'savgol':
        # Ensure window_size is odd
        if window_size % 2 == 0:
            window_size += 1
        
        # Ensure polyorder < window_size
        polyorder = min(polyorder, window_size - 1)
        
        smoothed = savgol_filter(temperature, window_size, polyorder)
    
    elif method == 'moving_avg':
        # Simple moving average
        kernel = np.ones(window_size) / window_size
        smoothed = np.convolve(temperature, kernel, mode='same')
        
        # Fix edge effects
        half_window = window_size // 2
        for i in range(half_window):
            smoothed[i] = np.mean(temperature[:i+half_window+1])
            smoothed[-(i+1)] = np.mean(temperature[-(i+half_window+1):])
    
    else:
        raise ValueError(f"Unknown method '{method}'. Use 'savgol' or 'moving_avg'")
    
    return smoothed


def detect_soak_zones(
    time: np.ndarray,
    temperature: np.ndarray,
    tolerance: float = 2.0,
    min_duration: float = 5.0
) -> List[Dict[str, Union[int, float]]]:
    """
    Detect temperature soak zones (plateaus) in thermal cycle data.
    
    A soak zone is defined as a period where temperature variation stays
    within tolerance for at least min_duration.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        tolerance: Maximum temperature change (°C) per step to consider as soak (default: 2.0)
        min_duration: Minimum duration (time units) to qualify as soak (default: 5.0)
    
    Returns:
        List of dictionaries containing soak zone information:
        - 'start_idx': Starting index
        - 'end_idx': Ending index
        - 'start_time': Start time
        - 'end_time': End time
        - 'duration': Duration of soak
        - 'avg_temp': Average temperature during soak
        - 'temp_std': Temperature standard deviation
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = np.concatenate([20 + 0.5*time[:300], 170*np.ones(400), 170 - 0.5*time[700:]])
        >>> soaks = detect_soak_zones(time, temp, tolerance=2.0, min_duration=10)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    temperature = np.array(temperature)
    time = np.array(time)
    
    # Calculate rate of change (absolute temperature difference between consecutive points)
    dT = np.abs(np.diff(temperature))
    
    soak_zones = []
    start = None
    
    for i in range(len(dT)):
        if dT[i] <= tolerance:
            if start is None:
                start = i
        else:
            if start is not None:
                length = i - start
                if length >= min_duration:
                    zone_t = time[start:i+1]
                    zone_temp = temperature[start:i+1]
                    soak_zones.append({
                        'start_idx': start,
                        'end_idx': i,
                        'start_time': float(zone_t[0]),
                        'end_time': float(zone_t[-1]),
                        'duration': float(zone_t[-1] - zone_t[0]),
                        'avg_temp': float(np.mean(zone_temp)),
                        'temp_std': float(np.std(zone_temp))
                    })
                start = None
    
    # Check if profile ends inside a soak
    if start is not None:
        i = len(dT)
        length = i - start
        if length >= min_duration:
            zone_t = time[start:i+1]
            zone_temp = temperature[start:i+1]
            soak_zones.append({
                'start_idx': start,
                'end_idx': i,
                'start_time': float(zone_t[0]),
                'end_time': float(zone_t[-1]),
                'duration': float(zone_t[-1] - zone_t[0]),
                'avg_temp': float(np.mean(zone_temp)),
                'temp_std': float(np.std(zone_temp))
            })
    
    return soak_zones



def segment_thermal_cycle(
    time: np.ndarray,
    temperature: np.ndarray,
    rate_threshold: float = 0.5
) -> List[Dict[str, Union[str, int, float]]]:
    """
    Segment a thermal cycle into distinct stages: ramp-up, soak, ramp-down, cool.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        rate_threshold: Minimum absolute ramp rate (°C/min) to classify as heating/cooling
                       (default: 0.5)
    
    Returns:
        List of dictionaries containing stage information:
        - 'stage_type': 'ramp_up', 'soak', 'ramp_down', or 'cool'
        - 'start_idx': Starting index
        - 'end_idx': Ending index
        - 'start_time': Start time
        - 'end_time': End time
        - 'start_temp': Starting temperature
        - 'end_temp': Ending temperature
        - 'duration': Stage duration
        - 'avg_rate': Average ramp rate (0 for soak stages)
    
    Example:
        >>> time = np.linspace(0, 200, 2000)
        >>> temp = np.piecewise(time, 
        ...     [time < 50, (time >= 50) & (time < 100), time >= 100],
        ...     [lambda t: 20 + 3*t, 170, lambda t: 170 - 2*(t-100)])
        >>> stages = segment_thermal_cycle(time, temp)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    # Calculate ramp rates
    rates = calculate_ramp_rate(time, temperature, window_size=5)
    
    stages = []
    current_stage_type = None
    stage_start_idx = 0
    
    for i in range(len(rates)):
        # Classify current point
        if rates[i] > rate_threshold:
            stage_type = 'ramp_up'
        elif rates[i] < -rate_threshold:
            # Distinguish between controlled ramp-down and cooling
            if temperature[i] > np.mean(temperature) * 0.7:
                stage_type = 'ramp_down'
            else:
                stage_type = 'cool'
        else:
            stage_type = 'soak'
        
        # Check if stage type changed
        if stage_type != current_stage_type and current_stage_type is not None:
            # Save previous stage
            stage_end_idx = i - 1
            duration = time[stage_end_idx] - time[stage_start_idx]
            avg_rate = np.mean(rates[stage_start_idx:stage_end_idx+1])
            
            stages.append({
                'stage_type': current_stage_type,
                'start_idx': stage_start_idx,
                'end_idx': stage_end_idx,
                'start_time': time[stage_start_idx],
                'end_time': time[stage_end_idx],
                'start_temp': temperature[stage_start_idx],
                'end_temp': temperature[stage_end_idx],
                'duration': duration,
                'avg_rate': avg_rate
            })
            
            stage_start_idx = i
        
        current_stage_type = stage_type
    
    # Add final stage
    if current_stage_type is not None:
        stage_end_idx = len(rates) - 1
        duration = time[stage_end_idx] - time[stage_start_idx]
        avg_rate = np.mean(rates[stage_start_idx:stage_end_idx+1])
        
        stages.append({
            'stage_type': current_stage_type,
            'start_idx': stage_start_idx,
            'end_idx': stage_end_idx,
            'start_time': time[stage_start_idx],
            'end_time': time[stage_end_idx],
            'start_temp': temperature[stage_start_idx],
            'end_temp': temperature[stage_end_idx],
            'duration': duration,
            'avg_rate': avg_rate
        })
    
    return stages
