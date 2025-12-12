"""
Anomaly Detection Module

This module provides functions for detecting anomalies in thermal cycle data:
- Temperature spike detection
- Overshoot detection
- Ramp rate anomalies
- Statistical anomaly detection
"""

import numpy as np
from typing import List, Dict, Union, Tuple, Optional
from scipy import stats


def detect_temperature_spikes(
    time: np.ndarray,
    temperature: np.ndarray,
    threshold_std: float = 3.0,
    window_size: int = 10
) -> List[Dict[str, Union[int, float]]]:
    """
    Detect temperature spikes using statistical methods.
    
    A spike is defined as a point that deviates from the local mean by more than
    threshold_std standard deviations.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        threshold_std: Number of standard deviations for spike detection (default: 3.0)
        window_size: Size of rolling window for local statistics (default: 10)
    
    Returns:
        List of dictionaries containing spike information:
        - 'index': Array index of spike
        - 'time': Time of spike
        - 'temperature': Temperature at spike
        - 'deviation': Number of standard deviations from local mean
        - 'local_mean': Local mean temperature
        - 'local_std': Local standard deviation
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = 500 + np.random.normal(0, 2, 1000)
        >>> temp[500] = 550  # Insert spike
        >>> spikes = detect_temperature_spikes(time, temp, threshold_std=3.0)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    if len(temperature) < window_size:
        raise ValueError(f"Data length must be >= window_size ({window_size})")
    
    spikes = []
    half_window = window_size // 2
    
    for i in range(half_window, len(temperature) - half_window):
        # Calculate local statistics
        start_idx = i - half_window
        end_idx = i + half_window + 1
        local_data = temperature[start_idx:end_idx]
        
        # Exclude current point from statistics
        local_data_without_current = np.concatenate([
            local_data[:half_window],
            local_data[half_window+1:]
        ])
        
        local_mean = np.mean(local_data_without_current)
        local_std = np.std(local_data_without_current)
        
        if local_std == 0:
            continue
        
        # Calculate deviation
        deviation = abs(temperature[i] - local_mean) / local_std
        
        if deviation > threshold_std:
            spikes.append({
                'index': i,
                'time': time[i],
                'temperature': temperature[i],
                'deviation': deviation,
                'local_mean': local_mean,
                'local_std': local_std
            })
    
    return spikes


def detect_overshoot(
    time: np.ndarray,
    temperature: np.ndarray,
    target_temp: float,
    tolerance: float = 5.0,
    min_overshoot: float = 10.0
) -> List[Dict[str, Union[int, float]]]:
    """
    Detect temperature overshoots beyond target temperature.
    
    An overshoot occurs when temperature exceeds target by more than tolerance
    during a heating phase.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        target_temp: Target temperature (°C)
        tolerance: Acceptable overshoot tolerance (°C, default: 5.0)
        min_overshoot: Minimum overshoot magnitude to report (°C, default: 10.0)
    
    Returns:
        List of dictionaries containing overshoot information:
        - 'index': Array index of maximum overshoot
        - 'time': Time of maximum overshoot
        - 'temperature': Peak temperature
        - 'overshoot_amount': Amount above target (°C)
        - 'start_index': Index where overshoot began
        - 'end_index': Index where overshoot ended
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = np.minimum(600 + 20*np.sin(time/10), 620)
        >>> overshoots = detect_overshoot(time, temp, target_temp=600, tolerance=5)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    overshoots = []
    threshold = target_temp + tolerance
    
    # Find regions above threshold
    above_threshold = temperature > threshold
    
    if not np.any(above_threshold):
        return overshoots
    
    # Find continuous overshoot regions
    in_overshoot = False
    overshoot_start = 0
    
    for i in range(len(temperature)):
        if above_threshold[i] and not in_overshoot:
            # Start of overshoot region
            overshoot_start = i
            in_overshoot = True
        
        elif (not above_threshold[i] or i == len(temperature) - 1) and in_overshoot:
            # End of overshoot region
            overshoot_end = i - 1 if not above_threshold[i] else i
            
            # Find peak in this region
            region_temps = temperature[overshoot_start:overshoot_end+1]
            peak_idx_in_region = np.argmax(region_temps)
            peak_idx = overshoot_start + peak_idx_in_region
            
            overshoot_amount = temperature[peak_idx] - target_temp
            
            if overshoot_amount >= min_overshoot:
                overshoots.append({
                    'index': peak_idx,
                    'time': time[peak_idx],
                    'temperature': temperature[peak_idx],
                    'overshoot_amount': overshoot_amount,
                    'start_index': overshoot_start,
                    'end_index': overshoot_end
                })
            
            in_overshoot = False
    
    return overshoots


def detect_rate_anomalies(
    time: np.ndarray,
    temperature: np.ndarray,
    expected_rate: float,
    tolerance: float = 0.5,
    window_size: int = 10
) -> List[Dict[str, Union[int, float, str]]]:
    """
    Detect anomalies in heating/cooling rates.
    
    Identifies regions where the actual ramp rate deviates significantly from
    the expected rate.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        expected_rate: Expected ramp rate (°C/min, positive for heating, negative for cooling)
        tolerance: Acceptable deviation from expected rate (°C/min, default: 0.5)
        window_size: Window size for rate calculation (default: 10)
    
    Returns:
        List of dictionaries containing anomaly information:
        - 'index': Array index of anomaly
        - 'time': Time of anomaly
        - 'actual_rate': Actual ramp rate at this point
        - 'expected_rate': Expected ramp rate
        - 'deviation': Deviation from expected rate
        - 'anomaly_type': 'too_fast' or 'too_slow'
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = 20 + 5*time + 2*np.random.randn(1000)
        >>> anomalies = detect_rate_anomalies(time, temp, expected_rate=5.0, tolerance=1.0)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    anomalies = []
    
    # Calculate local ramp rates
    for i in range(window_size, len(temperature) - window_size):
        # Use linear regression over window to get rate
        window_time = time[i-window_size:i+window_size+1]
        window_temp = temperature[i-window_size:i+window_size+1]
        
        # Fit linear model
        coeffs = np.polyfit(window_time, window_temp, 1)
        actual_rate = coeffs[0]  # Slope
        
        deviation = abs(actual_rate - expected_rate)
        
        if deviation > tolerance:
            if actual_rate > expected_rate:
                anomaly_type = 'too_fast'
            else:
                anomaly_type = 'too_slow'
            
            anomalies.append({
                'index': i,
                'time': time[i],
                'actual_rate': actual_rate,
                'expected_rate': expected_rate,
                'deviation': deviation,
                'anomaly_type': anomaly_type
            })
    
    return anomalies


def statistical_anomaly_detection(
    data: np.ndarray,
    method: str = 'zscore',
    threshold: float = 3.0,
    return_scores: bool = False
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    """
    Detect anomalies using statistical methods.
    
    Args:
        data: 1D array of data values
        method: Detection method - 'zscore', 'iqr', or 'mad' (median absolute deviation)
        threshold: Threshold for anomaly detection (method-dependent)
                  - zscore: number of standard deviations (default: 3.0)
                  - iqr: IQR multiplier (default: 1.5)
                  - mad: MAD multiplier (default: 3.0)
        return_scores: If True, also return anomaly scores
    
    Returns:
        Boolean array indicating anomalies (True = anomaly)
        If return_scores=True, also returns array of anomaly scores
    
    Example:
        >>> data = np.random.normal(100, 5, 1000)
        >>> data[500] = 150  # Insert anomaly
        >>> is_anomaly = statistical_anomaly_detection(data, method='zscore', threshold=3.0)
    """
    if len(data) == 0:
        raise ValueError("Data array cannot be empty")
    
    if method == 'zscore':
        # Z-score method
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return np.zeros(len(data), dtype=bool)
        
        z_scores = np.abs((data - mean) / std)
        anomalies = z_scores > threshold
        scores = z_scores
    
    elif method == 'iqr':
        # Interquartile range method
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        anomalies = (data < lower_bound) | (data > upper_bound)
        
        # Calculate scores as distance from bounds
        scores = np.maximum(
            (lower_bound - data) / iqr,
            (data - upper_bound) / iqr
        )
        scores = np.maximum(scores, 0)
    
    elif method == 'mad':
        # Median Absolute Deviation method
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        
        if mad == 0:
            return np.zeros(len(data), dtype=bool)
        
        # Modified z-score using MAD
        modified_z_scores = 0.6745 * np.abs(data - median) / mad
        anomalies = modified_z_scores > threshold
        scores = modified_z_scores
    
    else:
        raise ValueError(f"Unknown method '{method}'. Use 'zscore', 'iqr', or 'mad'")
    
    if return_scores:
        return anomalies, scores
    else:
        return anomalies


def detect_gradient_anomalies(
    time: np.ndarray,
    temperature: np.ndarray,
    threshold_percentile: float = 95.0
) -> List[Dict[str, Union[int, float]]]:
    """
    Detect anomalies based on sudden changes in temperature gradient.
    
    Useful for identifying unexpected jumps or drops in temperature.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        threshold_percentile: Percentile threshold for gradient magnitude (default: 95.0)
    
    Returns:
        List of dictionaries containing gradient anomaly information:
        - 'index': Array index of anomaly
        - 'time': Time of anomaly
        - 'temperature': Temperature at anomaly
        - 'gradient': Temperature gradient magnitude
        - 'threshold': Threshold value used
    
    Example:
        >>> time = np.linspace(0, 100, 1000)
        >>> temp = 500 + 0.1*time
        >>> temp[500:505] += 50  # Insert sudden jump
        >>> anomalies = detect_gradient_anomalies(time, temp)
    """
    if len(time) != len(temperature):
        raise ValueError("time and temperature arrays must have the same length")
    
    # Calculate gradients
    dt = np.diff(time)
    dT = np.diff(temperature)
    
    # Avoid division by zero
    dt[dt == 0] = 1e-10
    
    gradients = np.abs(dT / dt)
    
    # Calculate threshold
    threshold = np.percentile(gradients, threshold_percentile)
    
    # Find anomalies
    anomalies = []
    anomaly_indices = np.where(gradients > threshold)[0]
    
    for idx in anomaly_indices:
        anomalies.append({
            'index': idx,
            'time': time[idx],
            'temperature': temperature[idx],
            'gradient': gradients[idx],
            'threshold': threshold
        })
    
    return anomalies
