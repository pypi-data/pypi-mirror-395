"""
Unit tests for brazing module
"""

import pytest
import numpy as np
from pydt_utils.brazing import (
    detect_liquidus_crossing,
    validate_brazing_stage,
    calculate_brazing_quality_score,
    check_thermal_budget
)


class TestDetectLiquidusCrossing:
    """Tests for detect_liquidus_crossing function"""
    
    def test_single_crossing(self):
        """Test detection of single heating crossing"""
        time = np.linspace(0, 100, 1000)
        temp = 20 + 5 * time  # Linear heating
        
        crossings = detect_liquidus_crossing(time, temp, liquidus_temp=450)
        
        # Should detect one heating crossing
        assert len(crossings) >= 1
        assert crossings[0]['crossing_type'] == 'heating'
        assert abs(crossings[0]['temperature'] - 450) < 1.0
    
    def test_heating_and_cooling(self):
        """Test detection of both heating and cooling crossings"""
        time = np.linspace(0, 200, 2000)
        temp = np.concatenate([
            20 + 5 * time[:1000],           # Heat to 520°C
            520 - 5 * (time[1000:] - 100)   # Cool back down
        ])
        
        crossings = detect_liquidus_crossing(time, temp, liquidus_temp=450)
        
        # Should detect heating and cooling crossings
        crossing_types = [c['crossing_type'] for c in crossings]
        assert 'heating' in crossing_types
        assert 'cooling' in crossing_types


class TestValidateBrazingStage:
    """Tests for validate_brazing_stage function"""
    
    def test_valid_stage(self):
        """Test validation of a good brazing stage"""
        time = np.linspace(0, 60, 600)
        temp = 600 * np.ones_like(time)  # Hold at 600°C for 60 min
        
        result = validate_brazing_stage(
            time, temp,
            target_temp=600,
            hold_time=30,
            temp_tolerance=5.0
        )
        
        assert result['valid'] is True
        assert result['actual_hold_time'] >= 30
    
    def test_insufficient_hold_time(self):
        """Test validation failure due to insufficient hold time"""
        time = np.linspace(0, 20, 200)
        temp = 600 * np.ones_like(time)  # Only 20 min hold
        
        result = validate_brazing_stage(
            time, temp,
            target_temp=600,
            hold_time=30,
            temp_tolerance=5.0
        )
        
        assert result['valid'] is False
    
    def test_temperature_never_reached(self):
        """Test when target temperature is never reached"""
        time = np.linspace(0, 60, 600)
        temp = 500 * np.ones_like(time)  # Too low
        
        result = validate_brazing_stage(
            time, temp,
            target_temp=600,
            hold_time=30,
            temp_tolerance=5.0
        )
        
        assert result['valid'] is False
        assert result['actual_hold_time'] == 0.0


class TestCalculateBrazingQualityScore:
    """Tests for calculate_brazing_quality_score function"""
    
    def test_perfect_cycle(self):
        """Test quality score for an ideal brazing cycle"""
        time = np.linspace(0, 100, 1000)
        
        # Create ideal cycle
        temp = np.zeros_like(time)
        temp[time < 30] = 20 + 15 * time[time < 30]  # Heat to 470°C
        temp[(time >= 30) & (time < 70)] = 600       # Hold at 600°C
        temp[time >= 70] = 600 - 10 * (time[time >= 70] - 70)  # Cool
        
        score = calculate_brazing_quality_score(
            time, temp,
            liquidus_temp=450,
            target_temp=600,
            target_hold_time=30
        )
        
        # Should have high overall score
        assert score['overall_score'] >= 70
        assert score['liquidus_score'] > 0
    
    def test_poor_cycle(self):
        """Test quality score for a poor brazing cycle"""
        time = np.linspace(0, 100, 1000)
        temp = 400 * np.ones_like(time)  # Never reaches liquidus
        
        score = calculate_brazing_quality_score(
            time, temp,
            liquidus_temp=450,
            target_temp=600,
            target_hold_time=30
        )
        
        # Should have low overall score
        assert score['overall_score'] < 50
        assert len(score['issues']) > 0


class TestCheckThermalBudget:
    """Tests for check_thermal_budget function"""
    
    def test_within_budget(self):
        """Test when all temperatures are within limits"""
        time = np.linspace(0, 100, 1000)
        temp = 500 + 50 * np.sin(time / 10)  # Oscillates between 450-550°C
        
        result = check_thermal_budget(time, temp, min_temp=400, max_temp=650)
        
        assert result['within_budget'] is True
        assert len(result['violations']) == 0
    
    def test_exceeds_maximum(self):
        """Test when temperature exceeds maximum"""
        time = np.linspace(0, 100, 1000)
        temp = 500 * np.ones_like(time)
        temp[500] = 700  # Spike above limit
        
        result = check_thermal_budget(time, temp, min_temp=400, max_temp=650)
        
        assert result['within_budget'] is False
        assert result['max_violation'] > 0
    
    def test_below_minimum(self):
        """Test when temperature falls below minimum"""
        time = np.linspace(0, 100, 1000)
        temp = 500 * np.ones_like(time)
        temp[500] = 300  # Drop below limit
        
        result = check_thermal_budget(time, temp, min_temp=400, max_temp=650)
        
        assert result['within_budget'] is False
        assert result['min_violation'] > 0
