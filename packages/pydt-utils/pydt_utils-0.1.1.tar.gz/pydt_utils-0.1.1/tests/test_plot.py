"""
Unit tests for plot module
"""

import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
from pydt_utils.plot import (
    plot_thermal_cycle,
    plot_brazing_stages,
    plot_with_anomalies,
    plot_temperature_distribution,
    create_cycle_comparison,
    plot_ramp_rate_analysis
)


class TestPlotThermalCycle:
    """Tests for plot_thermal_cycle function"""
    
    def test_basic_plot(self):
        """Test basic thermal cycle plotting"""
        time = np.linspace(0, 100, 100)
        temp = 20 + 5 * time
        
        fig = plot_thermal_cycle(time, temp, show=False)
        
        assert fig is not None
        assert len(fig.axes) == 1
    
    def test_with_stages(self):
        """Test plotting with stage annotations"""
        time = np.linspace(0, 100, 100)
        temp = 20 + 5 * time
        
        stages = [
            {
                'stage_type': 'ramp_up',
                'start_idx': 0,
                'end_idx': 50,
                'start_time': 0,
                'end_time': 50
            }
        ]
        
        fig = plot_thermal_cycle(time, temp, stages=stages, show=False)
        
        assert fig is not None


class TestPlotBrazingStages:
    """Tests for plot_brazing_stages function"""
    
    def test_basic_brazing_plot(self):
        """Test basic brazing stage plotting"""
        time = np.linspace(0, 100, 100)
        temp = 20 + 5 * time
        
        fig = plot_brazing_stages(
            time, temp,
            liquidus_temp=450,
            target_temp=600,
            show=False
        )
        
        assert fig is not None
        assert len(fig.axes) == 1


class TestPlotWithAnomalies:
    """Tests for plot_with_anomalies function"""
    
    def test_anomaly_plotting(self):
        """Test plotting with anomaly markers"""
        time = np.linspace(0, 100, 100)
        temp = 500 * np.ones_like(time)
        anomaly_indices = [10, 50, 90]
        
        fig = plot_with_anomalies(
            time, temp,
            anomaly_indices,
            anomaly_type="Spike",
            show=False
        )
        
        assert fig is not None
    
    def test_empty_anomalies(self):
        """Test plotting with no anomalies"""
        time = np.linspace(0, 100, 100)
        temp = 500 * np.ones_like(time)
        
        fig = plot_with_anomalies(
            time, temp,
            [],
            show=False
        )
        
        assert fig is not None


class TestPlotTemperatureDistribution:
    """Tests for plot_temperature_distribution function"""
    
    def test_single_distribution(self):
        """Test plotting single temperature distribution"""
        x = np.linspace(0, 0.1, 50)
        T = 600 * np.exp(-x / 0.02)
        
        fig = plot_temperature_distribution(
            x, T,
            time_labels='t=0',
            show=False
        )
        
        assert fig is not None
    
    def test_multiple_distributions(self):
        """Test plotting multiple temperature distributions"""
        x = np.linspace(0, 0.1, 50)
        T1 = 600 * np.exp(-x / 0.02)
        T2 = 400 * np.exp(-x / 0.02)
        
        fig = plot_temperature_distribution(
            x, [T1, T2],
            time_labels=['t=0', 't=100'],
            show=False
        )
        
        assert fig is not None


class TestCreateCycleComparison:
    """Tests for create_cycle_comparison function"""
    
    def test_multiple_cycles(self):
        """Test comparing multiple thermal cycles"""
        time1 = np.linspace(0, 100, 100)
        temp1 = 20 + 5 * time1
        
        time2 = np.linspace(0, 100, 100)
        temp2 = 20 + 3 * time2
        
        cycles = {
            'Fast Heating': (time1, temp1),
            'Slow Heating': (time2, temp2)
        }
        
        fig = create_cycle_comparison(cycles, show=False)
        
        assert fig is not None


class TestPlotRampRateAnalysis:
    """Tests for plot_ramp_rate_analysis function"""
    
    def test_ramp_rate_plot(self):
        """Test ramp rate analysis plotting"""
        time = np.linspace(0, 100, 100)
        temp = 20 + 5 * time
        rates = 5 * np.ones_like(time)
        
        fig = plot_ramp_rate_analysis(
            time, temp, rates,
            expected_rate=5.0,
            show=False
        )
        
        assert fig is not None
        assert len(fig.axes) == 2  # Should have 2 subplots
