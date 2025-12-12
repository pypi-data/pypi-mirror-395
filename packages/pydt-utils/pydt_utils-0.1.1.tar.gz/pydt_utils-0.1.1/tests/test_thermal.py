"""
Unit tests for thermal module
"""

import pytest
import numpy as np
from pydt_utils.thermal import (
    calculate_heat_flux,
    calculate_biot_number,
    estimate_cooling_time,
    solve_1d_diffusion,
    calculate_fourier_number,
    calculate_thermal_diffusivity,
    calculate_thermal_penetration_depth
)


class TestCalculateHeatFlux:
    """Tests for calculate_heat_flux function"""
    
    def test_positive_gradient(self):
        """Test with positive temperature gradient"""
        gradient = 100  # K/m
        k = 15  # W/m·K
        
        flux = calculate_heat_flux(gradient, k)
        
        # Flux should be negative (heat flows from hot to cold)
        assert flux == -1500
    
    def test_array_input(self):
        """Test with array of gradients"""
        gradients = np.array([50, 100, 150])
        k = 15
        
        fluxes = calculate_heat_flux(gradients, k)
        
        assert len(fluxes) == 3
        assert np.allclose(fluxes, -k * gradients)


class TestCalculateBiotNumber:
    """Tests for calculate_biot_number function"""
    
    def test_small_biot(self):
        """Test calculation resulting in small Biot number"""
        h = 10  # W/m²·K (natural convection)
        L = 0.001  # m (1 mm)
        k = 15  # W/m·K (steel)
        
        Bi = calculate_biot_number(h, L, k)
        
        # Should be << 1 (lumped capacitance valid)
        assert Bi < 0.1
    
    def test_large_biot(self):
        """Test calculation resulting in large Biot number"""
        h = 1000  # W/m²·K (forced convection)
        L = 0.1  # m (10 cm)
        k = 0.5  # W/m·K (poor conductor)
        
        Bi = calculate_biot_number(h, L, k)
        
        # Should be >> 1
        assert Bi > 10
    
    def test_zero_conductivity(self):
        """Test error handling for zero conductivity"""
        with pytest.raises(ValueError):
            calculate_biot_number(10, 0.01, 0)


class TestEstimateCoolingTime:
    """Tests for estimate_cooling_time function"""
    
    def test_basic_cooling(self):
        """Test basic cooling time estimation"""
        t_cool = estimate_cooling_time(
            T_initial=600,
            T_final=100,
            T_ambient=20,
            characteristic_length=0.01,
            alpha=4e-6,
            h=10,
            k=15
        )
        
        # Should return positive time
        assert t_cool > 0
    
    def test_invalid_temperatures(self):
        """Test error handling for invalid temperatures"""
        with pytest.raises(ValueError):
            estimate_cooling_time(
                T_initial=100,
                T_final=600,  # Final > Initial
                T_ambient=20,
                characteristic_length=0.01,
                alpha=4e-6
            )


class TestSolve1DDiffusion:
    """Tests for solve_1d_diffusion function"""
    
    def test_basic_diffusion(self):
        """Test basic 1D diffusion solution"""
        # Initial condition: hot spot in center
        x = np.linspace(0, 0.1, 50)
        T0 = 20 + 580 * np.exp(-((x - 0.05)**2) / 0.001)
        
        # Boundary conditions: fixed at 20°C
        bc = (('dirichlet', 20), ('dirichlet', 20))
        
        # Solve
        T_history, t = solve_1d_diffusion(
            T0, bc,
            time_steps=100,
            dx=0.002,
            dt=0.01,
            alpha=4e-6
        )
        
        # Temperature should decrease over time
        assert T_history[-1, 25] < T_history[0, 25]
    
    def test_stability_violation(self):
        """Test error for stability condition violation"""
        T0 = 100 * np.ones(50)
        bc = (('dirichlet', 20), ('dirichlet', 20))
        
        # Use unstable parameters (dt too large)
        with pytest.raises(ValueError):
            solve_1d_diffusion(
                T0, bc,
                time_steps=10,
                dx=0.001,
                dt=1.0,  # Too large
                alpha=4e-6
            )


class TestCalculateFourierNumber:
    """Tests for calculate_fourier_number function"""
    
    def test_basic_calculation(self):
        """Test basic Fourier number calculation"""
        alpha = 4e-6  # m²/s
        t = 100  # s
        L = 0.01  # m
        
        Fo = calculate_fourier_number(alpha, t, L)
        
        expected = (4e-6 * 100) / (0.01**2)
        assert abs(Fo - expected) < 1e-6
    
    def test_zero_length(self):
        """Test error handling for zero length"""
        with pytest.raises(ValueError):
            calculate_fourier_number(4e-6, 100, 0)


class TestCalculateThermalDiffusivity:
    """Tests for calculate_thermal_diffusivity function"""
    
    def test_steel_properties(self):
        """Test with typical steel properties"""
        k = 15  # W/m·K
        rho = 7850  # kg/m³
        cp = 500  # J/kg·K
        
        alpha = calculate_thermal_diffusivity(k, rho, cp)
        
        # Should be around 4e-6 m²/s for steel
        assert 3e-6 < alpha < 5e-6
    
    def test_zero_density(self):
        """Test error handling for zero density"""
        with pytest.raises(ValueError):
            calculate_thermal_diffusivity(15, 0, 500)


class TestCalculateThermalPenetrationDepth:
    """Tests for calculate_thermal_penetration_depth function"""
    
    def test_basic_calculation(self):
        """Test basic penetration depth calculation"""
        alpha = 4e-6  # m²/s
        t = 100  # s
        
        depth = calculate_thermal_penetration_depth(alpha, t)
        
        expected = np.sqrt(4e-6 * 100)
        assert abs(depth - expected) < 1e-6
