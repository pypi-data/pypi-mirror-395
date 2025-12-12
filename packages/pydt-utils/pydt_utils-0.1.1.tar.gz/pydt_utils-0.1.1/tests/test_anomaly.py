"""
Unit tests for anomaly module
"""

import pytest
import numpy as np
from pydt_utils.anomaly import (
    detect_temperature_spikes,
    detect_overshoot,
    detect_rate_anomalies,
    statistical_anomaly_detection,
    detect_gradient_anomalies
)


class TestDetectTemperatureSpikes:
    """Tests for detect_temperature_spikes function"""
    
    def test_single_spike(self):
        """Test detection of single temperature spike"""
        time = np.linspace(0, 100, 1000)
        temp = 500 + np.random.normal(0, 1, 1000)
        temp[500] = 550  # Insert spike
        
        spikes = detect_temperature_spikes(time, temp, threshold_std=3.0, window_size=10)
        
        # Should detect the spike
        assert len(spikes) > 0
        spike_indices = [s['index'] for s in spikes]
        assert 500 in spike_indices
    
    def test_no_spikes(self):
        """Test with clean data (no spikes)"""
        time = np.linspace(0, 100, 1000)
        temp = 500 + np.random.normal(0, 0.5, 1000)  # Low noise
        
        spikes = detect_temperature_spikes(time, temp, threshold_std=3.0)
        
        # Should detect few or no spikes
        assert len(spikes) < 10


class TestDetectOvershoot:
    """Tests for detect_overshoot function"""
    
    def test_single_overshoot(self):
        """Test detection of temperature overshoot"""
        time = np.linspace(0, 100, 1000)
        temp = np.minimum(600 + 20 * np.sin(time / 10), 620)
        
        overshoots = detect_overshoot(
            time, temp,
            target_temp=600,
            tolerance=5.0,
            min_overshoot=10.0
        )
        
        # Should detect overshoot
        assert len(overshoots) > 0
    
    def test_no_overshoot(self):
        """Test with no overshoot"""
        time = np.linspace(0, 100, 1000)
        temp = 590 * np.ones_like(time)  # Below target
        
        overshoots = detect_overshoot(
            time, temp,
            target_temp=600,
            tolerance=5.0
        )
        
        assert len(overshoots) == 0


class TestDetectRateAnomalies:
    """Tests for detect_rate_anomalies function"""
    
    def test_rate_deviation(self):
        """Test detection of ramp rate anomalies"""
        time = np.linspace(0, 100, 1000)
        temp = 20 + 5 * time  # Expected 5°C/min
        
        # Insert faster heating section
        temp[500:600] = temp[500] + 10 * (time[500:600] - time[500])
        
        anomalies = detect_rate_anomalies(
            time, temp,
            expected_rate=5.0,
            tolerance=1.0,
            window_size=10
        )
        
        # Should detect anomalies in the fast heating section
        assert len(anomalies) > 0


class TestStatisticalAnomalyDetection:
    """Tests for statistical_anomaly_detection function"""
    
    def test_zscore_method(self):
        """Test Z-score anomaly detection"""
        data = np.random.normal(100, 5, 1000)
        data[500] = 150  # Insert anomaly
        
        anomalies = statistical_anomaly_detection(
            data,
            method='zscore',
            threshold=3.0
        )
        
        # Should detect the anomaly
        assert anomalies[500] is True
    
    def test_iqr_method(self):
        """Test IQR anomaly detection"""
        data = np.random.normal(100, 5, 1000)
        data[500] = 200  # Insert anomaly
        
        anomalies = statistical_anomaly_detection(
            data,
            method='iqr',
            threshold=1.5
        )
        
        # Should detect the anomaly
        assert anomalies[500] is True
    
    def test_mad_method(self):
        """Test MAD anomaly detection"""
        data = np.random.normal(100, 5, 1000)
        data[500] = 150  # Insert anomaly
        
        anomalies = statistical_anomaly_detection(
            data,
            method='mad',
            threshold=3.0
        )
        
        # Should detect the anomaly
        assert anomalies[500] is True
    
    def test_return_scores(self):
        """Test returning anomaly scores"""
        data = np.random.normal(100, 5, 100)
        
        anomalies, scores = statistical_anomaly_detection(
            data,
            method='zscore',
            threshold=3.0,
            return_scores=True
        )
        
        assert len(scores) == len(data)
        assert len(anomalies) == len(data)
    
    def test_invalid_method(self):
        """Test error handling for invalid method"""
        data = np.random.randn(100)
        
        with pytest.raises(ValueError):
            statistical_anomaly_detection(data, method='invalid')


class TestDetectGradientAnomalies:
    """Tests for detect_gradient_anomalies function"""
    
    def test_sudden_jump(self):
        """Test detection of sudden temperature jump"""
        time = np.linspace(0, 100, 1000)
        temp = 500 + 0.1 * time
        temp[500:] += 50  # Sudden jump
        
        anomalies = detect_gradient_anomalies(time, temp, threshold_percentile=95.0)
        
        # Should detect anomalies near the jump
        assert len(anomalies) > 0
        anomaly_indices = [a['index'] for a in anomalies]
        assert any(495 <= idx <= 505 for idx in anomaly_indices)
