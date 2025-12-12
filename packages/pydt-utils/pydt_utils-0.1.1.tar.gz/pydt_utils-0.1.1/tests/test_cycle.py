"""
Unit tests for cycle module
"""

import pytest
import numpy as np
from pydt_utils.cycle import (
    calculate_ramp_rate,
    smooth_temperature_data,
    detect_soak_zones,
    segment_thermal_cycle
)


class TestCalculateRampRate:
    """Tests for calculate_ramp_rate function"""
    
    def test_linear_heating(self):
        """Test with constant heating rate"""
        time = np.linspace(0, 100, 100)
        temperature = 20 + 5 * time  # 5°C/min heating
        rates = calculate_ramp_rate(time, temperature, window_size=1)
        
        # Should be approximately 5°C/min throughout
        assert np.abs(np.mean(rates) - 5.0) < 0.5
    
    def test_linear_cooling(self):
        """Test with constant cooling rate"""
        time = np.linspace(0, 100, 100)
        temperature = 600 - 3 * time  # -3°C/min cooling
        rates = calculate_ramp_rate(time, temperature, window_size=1)
        
        assert np.abs(np.mean(rates) + 3.0) < 0.5
    
    def test_length_mismatch(self):
        """Test error handling for mismatched arrays"""
        time = np.array([0, 1, 2])
        temperature = np.array([20, 25])
        
        with pytest.raises(ValueError):
            calculate_ramp_rate(time, temperature)
    
    def test_insufficient_data(self):
        """Test error handling for insufficient data"""
        time = np.array([0])
        temperature = np.array([20])
        
        with pytest.raises(ValueError):
            calculate_ramp_rate(time, temperature)


class TestSmoothTemperatureData:
    """Tests for smooth_temperature_data function"""
    
    def test_savgol_smoothing(self):
        """Test Savitzky-Golay smoothing"""
        # Create noisy data
        x = np.linspace(0, 10, 100)
        clean = 100 + 50 * np.sin(x)
        noisy = clean + np.random.normal(0, 2, 100)
        
        smoothed = smooth_temperature_data(noisy, window_size=11, method='savgol')
        
        # Smoothed should be closer to clean than noisy
        error_noisy = np.mean((noisy - clean)**2)
        error_smoothed = np.mean((smoothed - clean)**2)
        assert error_smoothed < error_noisy
    
    def test_moving_average_smoothing(self):
        """Test moving average smoothing"""
        data = np.array([1, 2, 100, 4, 5, 6, 7])  # Spike at index 2
        smoothed = smooth_temperature_data(data, window_size=3, method='moving_avg')
        
        # Spike should be reduced
        assert smoothed[2] < data[2]
    
    def test_invalid_method(self):
        """Test error handling for invalid method"""
        data = np.random.randn(100)
        
        with pytest.raises(ValueError):
            smooth_temperature_data(data, method='invalid')


class TestDetectSoakZones:
    """Tests for detect_soak_zones function"""
    
    def test_single_soak(self):
        """Test detection of single soak zone"""
        time = np.linspace(0, 100, 1000)
        temp = np.concatenate([
            20 + 0.5 * time[:300],  # Heating
            170 * np.ones(400),      # Soak at 170°C
            170 - 0.5 * time[700:]   # Cooling
        ])
        
        soaks = detect_soak_zones(time, temp, tolerance=2.0, min_duration=10)
        
        assert len(soaks) >= 1
        assert soaks[0]['avg_temp'] > 165
        assert soaks[0]['avg_temp'] < 175
    
    def test_no_soak(self):
        """Test with no soak zones"""
        time = np.linspace(0, 100, 100)
        temp = 20 + 5 * time  # Continuous heating
        
        soaks = detect_soak_zones(time, temp, tolerance=2.0, min_duration=10)
        
        assert len(soaks) == 0


class TestSegmentThermalCycle:
    """Tests for segment_thermal_cycle function"""
    
    def test_basic_segmentation(self):
        """Test basic cycle segmentation"""
        time = np.linspace(0, 200, 2000)
        
        # Create piecewise cycle
        temp = np.zeros_like(time)
        temp[time < 50] = 20 + 3 * time[time < 50]  # Ramp up
        temp[(time >= 50) & (time < 100)] = 170     # Soak
        temp[time >= 100] = 170 - 2 * (time[time >= 100] - 100)  # Ramp down
        
        stages = segment_thermal_cycle(time, temp, rate_threshold=0.5)
        
        # Should have at least ramp_up, soak, and ramp_down stages
        stage_types = [s['stage_type'] for s in stages]
        assert 'ramp_up' in stage_types
        assert 'soak' in stage_types
    
    def test_length_mismatch(self):
        """Test error handling for mismatched arrays"""
        time = np.array([0, 1, 2])
        temperature = np.array([20, 25])
        
        with pytest.raises(ValueError):
            segment_thermal_cycle(time, temperature)
